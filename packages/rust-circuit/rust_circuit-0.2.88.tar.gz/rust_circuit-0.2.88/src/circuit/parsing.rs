use super::{
    Add, ArrayConstant, Concat, Einsum, GeneralFunction, Index, Rearrange, ScalarConstant, Scatter,
    Symbol,
};
use super::{CircuitConstructionError, CircuitRc};
use crate::all_imports::{Shape, Sv, TensorIndex};
use crate::circuit::{
    AutoTag, CircResult, CircuitNode, Cumulant, DiscreteVar, ModuleNode, ModuleNodeSpec,
    StoredCumulantVar,
};
use crate::hashmaps::FxHashMap as HashMap;
use crate::pyo3_prelude::*;
use crate::tensor_util::TorchDeviceDtypeOp;
use once_cell::sync::Lazy;
use regex::Regex;
use std::iter::zip;
use std::rc::Rc;
use std::str::FromStr;
use std::sync::Arc;
use uuid::Uuid;

#[pyfunction(
    string,
    module_spec_map = "HashMap::new()",
    reference_circuits = "HashMap::new()",
    tensors_as_random = "false",
    tensors_as_random_device_dtype = "TorchDeviceDtypeOp{device:None,dtype:None}"
)]
pub fn parse_compiler_repr_bijection(
    string: &str,
    module_spec_map: HashMap<String, ModuleNodeSpec>,
    reference_circuits: HashMap<String, CircuitRc>,
    tensors_as_random: bool,
    tensors_as_random_device_dtype: TorchDeviceDtypeOp,
) -> Result<CircuitRc, CircuitConstructionError> {
    let string = string.trim();
    let lines: Vec<_> = string.lines().collect();
    // make seperate struct that can deeply mutate, can't use immutable Circuit bc see children later
    #[derive(Debug, Clone)]
    struct PartialCirc {
        pub variant: String, // copying bc refs annoying / don't care
        pub extra: String,
        pub shape: Option<Shape>,
        pub name: Option<String>,
        pub children: Vec<usize>,
    }
    let tab_width: usize = 2;
    let mut partial_circuits: Vec<Option<PartialCirc>> = vec![None; lines.len()];
    let mut stack: Vec<usize> = vec![];
    static RE: Lazy<Regex> = Lazy::new(|| {
        Regex::new(r"^( *)(\d+)(?: '((?:(?:\\')?[^']*)*)')?(?: \[([\d, ]*)\])?(?: ([a-zA-Z]+))?(?: (.*))?\s*$").unwrap()
    });
    for line in lines {
        let rf = || CircuitConstructionError::ParsingNoRegexMatch {
            line: line.to_owned(),
        };
        let re_captures = RE.captures(line).ok_or_else(rf)?;
        let num_spaces = re_captures.get(1).ok_or_else(rf)?.as_str().len();
        if num_spaces % tab_width != 0 {
            return Err(CircuitConstructionError::ParsingInvalidIndentation {
                tab_width: tab_width,
                spaces: num_spaces,
                stack_indentation: stack.len(),
                stack_top: stack
                    .last()
                    .map(|z| partial_circuits[*z].clone().unwrap().variant.clone()),
            });
        }
        let indentation_level = num_spaces / tab_width;
        if indentation_level > stack.len() {
            return Err(CircuitConstructionError::ParsingInvalidIndentation {
                tab_width: tab_width,
                spaces: num_spaces,
                stack_indentation: stack.len(),
                stack_top: stack
                    .last()
                    .map(|z| partial_circuits[*z].clone().unwrap().variant.clone()),
            });
        }
        stack.truncate(indentation_level);
        let serial_number = re_captures
            .get(2)
            .ok_or_else(rf)?
            .as_str()
            .parse::<usize>()
            .unwrap();

        if serial_number > partial_circuits.len() - 1 {
            partial_circuits.resize(serial_number + 1, None)
        }
        let is_new_node = partial_circuits[serial_number].is_none();
        if is_new_node {
            partial_circuits[serial_number] = Some(PartialCirc {
                name: re_captures
                    .get(3)
                    .map(|x| x.as_str().replace(r"\'", "'").replace(r"\\", r"\")),
                shape: if re_captures.get(4).is_some() {
                    Some(
                        re_captures
                            .get(4)
                            .ok_or_else(rf)?
                            .as_str()
                            .split(',')
                            .map(|z| z.trim())
                            .filter(|z| !z.is_empty())
                            .map(|x| x.parse::<usize>())
                            .collect::<Result<Sv<_>, _>>()
                            .map_err(|e| CircuitConstructionError::ParsingNumberFail {
                                string: format!("{}", e),
                            })?,
                    )
                } else {
                    None
                },
                variant: re_captures.get(5).ok_or_else(rf)?.as_str().to_owned(),
                extra: re_captures
                    .get(6)
                    .map(|z| z.as_str())
                    .unwrap_or("")
                    .trim()
                    .to_owned(),
                children: vec![],
            });
        }
        if let Some(l) = stack.last() {
            partial_circuits[*l]
                .as_mut()
                .unwrap()
                .children
                .push(serial_number);
        }
        if is_new_node {
            stack.push(serial_number);
        }
    }

    fn deep_convert_partial_circ(
        serial_number: usize,
        partial_circuits: &Vec<Option<PartialCirc>>,
        context: &mut HashMap<usize, CircuitRc>,
        module_spec_map: &HashMap<String, ModuleNodeSpec>,
        reference_circuits: &HashMap<String, CircuitRc>,
        tensors_as_random: bool,
        tensors_as_random_device_dtype: TorchDeviceDtypeOp,
    ) -> CircResult {
        if let Some(already) = context.get(&serial_number) {
            return Ok(already.clone());
        }
        if serial_number > partial_circuits.len() - 1 {
            return Err(CircuitConstructionError::ParsingInvalidSerialNumber { serial_number });
        }
        let ps = partial_circuits[serial_number]
            .as_ref()
            .ok_or(CircuitConstructionError::ParsingInvalidSerialNumber { serial_number })?;
        let children: Vec<CircuitRc> = ps
            .children
            .iter()
            .map(|x| {
                deep_convert_partial_circ(
                    *x,
                    partial_circuits,
                    context,
                    module_spec_map,
                    reference_circuits,
                    tensors_as_random,
                    tensors_as_random_device_dtype.clone(),
                )
            })
            .collect::<Result<Vec<_>, _>>()?;
        let variant: &str = &ps.variant;
        let result = match variant {
            "Array" => {
                if tensors_as_random {
                    Ok(ArrayConstant::randn_named(
                        ps.shape
                            .clone()
                            .ok_or(CircuitConstructionError::ParsingShapeNeeded {
                                variant: variant.to_owned(),
                            })?,
                        ps.name.clone(),
                        tensors_as_random_device_dtype,
                    )
                    .rc())
                } else {
                    ArrayConstant::from_hash_prefix(ps.name.clone(), &ps.extra)
                        .map(|z| z.rc())
                        .map_err(|e| CircuitConstructionError::PythonError {
                            py_err: Arc::new(e),
                        })
                }
            }
            "Scalar" => Ok(ScalarConstant::nrc(
                ps.extra.parse::<f64>().map_err(|e| {
                    CircuitConstructionError::ParsingNumberFail {
                        string: format!("{}", e),
                    }
                })?,
                ps.shape
                    .as_ref()
                    .ok_or(CircuitConstructionError::ParsingShapeNeeded {
                        variant: variant.to_owned(),
                    })?
                    .clone(),
                ps.name.clone(),
            )),
            "Add" => {
                if !ps.extra.is_empty() {
                    Err(CircuitConstructionError::ParsingExtraUnneededString {
                        string: ps.extra.to_owned(),
                    })
                } else {
                    Add::try_new(children, ps.name.clone()).map(|z| z.rc())
                }
            }
            "Concat" => Concat::try_new(
                children,
                ps.extra.parse::<usize>().map_err(|e| {
                    CircuitConstructionError::ParsingNumberFail {
                        string: format!("{}", e),
                    }
                })?,
                ps.name.clone(),
            )
            .map(|z| z.rc()),
            "Einsum" => {
                Einsum::from_einsum_string(&ps.extra, children, ps.name.clone()).map(|z| z.rc())
            }
            "Rearrange" => {
                Rearrange::from_einops_string(children[0].clone(), &ps.extra, ps.name.clone())
                    .map(|z| z.rc())
            }
            "Symbol" => {
                let shape = ps
                    .shape
                    .as_ref()
                    .ok_or(CircuitConstructionError::ParsingShapeNeeded {
                        variant: variant.to_owned(),
                    })?
                    .clone();
                if ps.extra.is_empty() {
                    Ok(Symbol::new_with_none_uuid(shape, ps.name.clone()).rc())
                } else {
                    Ok(Symbol::nrc(
                        shape,
                        Uuid::from_str(&ps.extra).map_err(|_e| {
                            CircuitConstructionError::ParsingFail {
                                string: ps.extra.to_owned(),
                            }
                        })?,
                        ps.name.clone(),
                    ))
                }
            }
            "GeneralFunction" => {
                GeneralFunction::new_by_name(children, ps.extra.clone(), ps.name.clone())
                    .map(|z| z.rc())
            }
            "Index" => Index::try_new(
                children[0].clone(),
                TensorIndex::from_bijection_string(&ps.extra)?,
                ps.name.clone(),
            )
            .map(|z| z.rc()),
            "Scatter" => Scatter::try_new(
                children[0].clone(),
                TensorIndex::from_bijection_string(&ps.extra)?,
                ps.shape
                    .as_ref()
                    .ok_or(CircuitConstructionError::ParsingShapeNeeded {
                        variant: variant.to_owned(),
                    })?
                    .clone(),
                ps.name.clone(),
            )
            .map(|z| z.rc()),
            "ModuleNode" => ModuleNode::try_new(
                children,
                module_spec_map
                    .get(&ps.extra.clone())
                    .cloned()
                    .ok_or_else(|| CircuitConstructionError::ModuleNotFound {
                        name: ps.extra.clone(),
                    })?,
                ps.name.clone(),
            )
            .map(|z| z.rc()),
            "Ref" => reference_circuits
                .get(&ps.extra.clone())
                .cloned()
                .ok_or_else(|| CircuitConstructionError::CircuitRefNotFound {
                    name: ps.extra.clone(),
                }),
            "AutoTag" => Uuid::from_str(&ps.extra)
                .map_err(|_| CircuitConstructionError::InvalidUuid {
                    string: ps.extra.clone(),
                })
                .map(|uuid| AutoTag::nrc(children[0].clone(), uuid, ps.name.clone())),
            "Cumulant" => Ok(Cumulant::nrc(children, ps.name.clone())),
            "DiscreteVar" => {
                DiscreteVar::try_new(children[0].clone(), children[1].clone(), ps.name.clone())
                    .map(|z| z.rc())
            }
            "StoredCumulantVar" => {
                if let [cum_nums, uuid] = ps.extra.split("|").collect::<Vec<_>>()[..] {
                    cum_nums
                        .split(",")
                        .map(|s| s.trim().parse::<usize>())
                        .collect::<Result<Vec<_>, _>>()
                        .map_err(|e| CircuitConstructionError::ParsingNumberFail {
                            string: format!("{}", e),
                        })
                        .and_then(|keys| {
                            Uuid::from_str(uuid)
                                .map_err(|_| CircuitConstructionError::InvalidUuid {
                                    string: ps.extra.clone(),
                                })
                                .map(|uuid| (keys, uuid))
                        })
                        .and_then(|(keys, uuid)| {
                            if keys.len() != children.len() {
                                Err(CircuitConstructionError::ParsingWrongNumberChildren {
                                    expected: keys.len(),
                                    found: children.len(),
                                })
                            } else {
                                StoredCumulantVar::try_new(
                                    zip(keys, children).collect(),
                                    uuid,
                                    ps.name.clone(),
                                )
                                .map(|z| z.rc())
                            }
                        })
                } else {
                    Err(CircuitConstructionError::ParsingFail {
                        string: ps.extra.clone(),
                    })
                }
            }
            _ => Err(CircuitConstructionError::ParsingInvalidVariant {
                v: variant.to_owned(),
            }),
        };
        if result.is_ok() {
            context.insert(serial_number, result.clone().unwrap());
        }
        result
    }
    let mut context: HashMap<usize, CircuitRc> = HashMap::new();
    deep_convert_partial_circ(
        stack[0],
        &partial_circuits,
        &mut context,
        &module_spec_map,
        &reference_circuits,
        tensors_as_random,
        tensors_as_random_device_dtype,
    )
}
