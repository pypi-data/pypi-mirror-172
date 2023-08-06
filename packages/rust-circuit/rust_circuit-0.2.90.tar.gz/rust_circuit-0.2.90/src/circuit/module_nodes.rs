use crate::all_imports::{TensorAxisIndex, TensorIndex};
use crate::circuit::deep_map_fallible_pre_new_children;
use crate::hashmaps::FxHashMap as HashMap;

use crate::{pycall, pyo3_prelude::*, sv};
use once_cell::sync::Lazy;
use regex::Regex;
use std::iter::zip;

use super::circuit_manipulation::replace_nodes;

use super::{
    deep_map_op_context, deep_map_op_context_preorder_stoppable, deep_map_unwrap, prelude::*, Add,
    CachedCircuitInfo, CircResult, Concat, GeneralFunction, HashBytes, Index, Rearrange, Scatter,
};

use crate::{
    circuit::{Einsum, PyCircuitBase, Symbol},
    circuit_node_auto_impl, circuit_node_extra_impl, new_rc_unwrap,
    tensor_util::{Shape, TorchDeviceDtype},
};

use macro_rules_attribute::apply;
use pyo3::types::PyDict;

use uuid::{uuid, Uuid};

#[pyfunction]
#[pyo3(name = "expand_node")]
pub fn expand_node_py(circuit: CircuitRc, inputs: Vec<CircuitRc>) -> CircResult {
    expand_node(circuit, &inputs)
}

pub fn expand_node(circuit: CircuitRc, inputs: &Vec<CircuitRc>) -> CircResult {
    if inputs.len() != circuit.children().count() {
        return Err(CircuitConstructionError::ModuleNodeWrongNumberChildren {
            expected: circuit.children().count(),
            got: inputs.len(),
        });
    }
    let batch_ranks: Vec<usize> = zip(circuit.children(), inputs)
        .filter_map(|(old, new)| new.info().rank().checked_sub(old.info().rank()))
        .collect();
    if batch_ranks.len() != inputs.len() {
        return Err(CircuitConstructionError::BatchingRankTooLow {
            default: circuit.children().map(|x| x.info().rank()).collect(),
            got: inputs.iter().map(|x| x.info().rank()).collect(),
        });
    }
    let batch_shapes: Vec<&[usize]> = zip(&batch_ranks, inputs)
        .map(|(br, new)| &new.info().shape[0..*br])
        .collect();
    match &**circuit {
        Circuit::Symbol(_) | Circuit::ScalarConstant(_) => Ok(circuit.clone()),
        Circuit::Rearrange(node) => {
            let input_shape_non_batch = inputs[0].info().shape[batch_ranks[0]..]
                .iter()
                .cloned()
                .collect();
            let new_spec = node
                .spec
                .conform_to_input_shape(&input_shape_non_batch, true)
                .map_err(|_e| CircuitConstructionError::RearrangeWrongInputShape {
                    spec: node.spec.clone(),
                    shape: input_shape_non_batch.clone(),
                })?
                .add_batch_dims(batch_ranks[0]);
            Ok(Rearrange::nrc(
                inputs[0].clone(),
                new_spec,
                circuit.name_cloned(),
            ))
        }
        Circuit::Index(node) => {
            // for now non-batch non-identity dims can't change
            for i in 0..node.node.info().rank() {
                if node.node.info().shape[i] != inputs[0].info().shape[i + batch_ranks[0]]
                    && node.index.0[i] != TensorAxisIndex::IDENT
                {
                    return Err(CircuitConstructionError::ExpandingFixedIndex {
                        index: node.index.clone(),
                        old_shape: node.node.info().shape.clone(),
                        new_shape: inputs[0].info().shape.clone(),
                    });
                }
            }
            Ok(Index::nrc(
                inputs[0].clone(),
                TensorIndex(
                    vec![TensorAxisIndex::IDENT; batch_ranks[0]]
                        .into_iter()
                        .chain(node.index.0.iter().cloned())
                        .collect(),
                ),
                node.name_cloned(),
            ))
        }
        Circuit::Scatter(node) => {
            // for now non-batch non-identity dims can't change
            for i in 0..node.node.info().rank() {
                if node.node.info().shape[i] != inputs[0].info().shape[i + batch_ranks[0]]
                    && node.index.0[i] != TensorAxisIndex::IDENT
                {
                    return Err(CircuitConstructionError::ExpandingFixedIndex {
                        index: node.index.clone(),
                        old_shape: node.node.info().shape.clone(),
                        new_shape: inputs[0].info().shape.clone(),
                    });
                }
            }
            Ok(Scatter::nrc(
                inputs[0].clone(),
                TensorIndex(
                    vec![TensorAxisIndex::IDENT; batch_ranks[0]]
                        .into_iter()
                        .chain(node.index.0.iter().cloned())
                        .collect(),
                ),
                inputs[0].info().shape[0..batch_ranks[0]]
                    .iter()
                    .cloned()
                    .chain(node.info().shape.iter().cloned())
                    .collect(),
                node.name_cloned(),
            ))
        }
        Circuit::Concat(node) => {
            if !batch_shapes.iter().all(|x| x == &batch_shapes[0]) {
                return Err(CircuitConstructionError::InconsistentBatches {
                    batch_shapes: batch_shapes
                        .iter()
                        .map(|x| x.iter().cloned().collect())
                        .collect(),
                    circuit: circuit.clone(),
                });
            }
            if !zip(&node.nodes, zip(inputs, &batch_ranks)).all(|(old, (new, br))| {
                old.info().shape[node.axis] == new.info().shape[node.axis + br]
            }) {
                return Err(CircuitConstructionError::ExpandingConcatAxis {
                    axis: node.axis,
                    old_shape: sv![],
                    new_shape: sv![],
                });
            }
            Concat::try_new(
                inputs.clone(),
                node.axis + batch_ranks[0],
                node.name_cloned(),
            )
            .map(|x| x.rc())
        }
        Circuit::Add(node) => Add::try_new(inputs.clone(), node.name_cloned()).map(|x| x.rc()),
        Circuit::GeneralFunction(node) => {
            GeneralFunction::try_new(inputs.clone(), node.spec.clone(), node.name_cloned())
                .map(|x| x.rc())
        }
        Circuit::Einsum(node) => {
            let mut batch_shape: Option<&[usize]> = None;
            for bs in &batch_shapes {
                if !bs.is_empty() {
                    if let Some(existing) = batch_shape {
                        if *bs != existing {
                            return Err(CircuitConstructionError::InconsistentBatches {
                                batch_shapes: batch_shapes
                                    .iter()
                                    .map(|x| x.iter().cloned().collect())
                                    .collect(),
                                circuit: circuit.clone(),
                            });
                        }
                    } else {
                        batch_shape = Some(bs.clone());
                    }
                }
            }
            let next_axis = node.next_axis();
            let newies = || (next_axis as u8..next_axis + batch_shape.unwrap().len() as u8);
            let out_axes = if let Some(_bs) = batch_shape {
                newies().chain(node.out_axes.iter().cloned()).collect()
            } else {
                node.out_axes.clone()
            };
            Einsum::try_new(
                node.args
                    .iter()
                    .enumerate()
                    .map(|(i, (_child, ints))| {
                        (inputs[i].clone(), {
                            if !batch_shapes[i].is_empty() {
                                newies().chain(ints.iter().cloned()).collect()
                            } else {
                                ints.clone()
                            }
                        })
                    })
                    .collect(),
                out_axes,
                node.name_cloned(),
            )
            .map(|x| x.rc())
        }
        Circuit::ModuleNode(node) => {
            ModuleNode::try_new(inputs.clone(), node.spec.clone(), node.name_cloned())
                .map(|z| z.rc())
        }
        _ => {
            if inputs[..] == circuit.children().collect::<Vec<_>>()[..] {
                Ok(circuit.clone())
            } else {
                Err(CircuitConstructionError::ExpandNodeUnknownVariant {
                    variant: circuit.variant_string(),
                })
            }
        }
    }
}

#[pyfunction]
#[pyo3(name = "replace_expand_bottom_up_dict")]
pub fn replace_expand_bottom_up_dict_py(
    circuit: CircuitRc,
    dict: HashMap<CircuitRc, CircuitRc>,
) -> CircResult {
    replace_expand_bottom_up(circuit, |x| dict.get(&x).cloned())
}

#[pyfunction]
#[pyo3(name = "replace_expand_bottom_up")]
pub fn replace_expand_bottom_up_py(circuit: CircuitRc, f: PyObject) -> CircResult {
    replace_expand_bottom_up(circuit, |x| pycall!(f, (x.clone(),)))
}

pub fn replace_expand_bottom_up<F>(
    circuit: CircuitRc,
    replacer: F,
) -> Result<CircuitRc, CircuitConstructionError>
where
    F: Fn(CircuitRc) -> Option<CircuitRc>,
{
    let recursor = |circuit: CircuitRc,
                    new_children: &Vec<CircuitRc>|
     -> Result<CircuitRc, CircuitConstructionError> {
        if let Some(replaced) = replacer(circuit.clone()) {
            return Ok(replaced);
        }
        expand_node(circuit, new_children)
    };
    deep_map_fallible_pre_new_children(circuit, recursor)
}

#[pyclass]
#[derive(Debug, Clone, PyClassDeriv, Hash, PartialEq, Eq)]
pub struct ModuleNodeSpec {
    #[pyo3(get)]
    pub spec_circuit: CircuitRc,
    #[pyo3(get)]
    pub input_specs: Vec<ModuleNodeArgSpec>,
    #[pyo3(get)]
    pub name: Option<String>,
}

impl ModuleNodeSpec {
    pub const EXPAND_PLACEHOLDER_UUID: Uuid = uuid!("741ba404-eec3-4ac9-b6ce-062e903fb033");
    pub fn expand_raw(&self, nodes: &Vec<CircuitRc>) -> CircResult {
        if self.input_specs.len() != nodes.len() {
            return Err(CircuitConstructionError::ModuleNodeWrongNumberChildren {
                expected: self.input_specs.len(),
                got: nodes.len(),
            });
        }
        for (spec, node) in zip(self.input_specs.iter(), nodes) {
            if node.info().rank() < spec.symbol.info().rank() {
                // todo error messages
                println!(
                    "node shapes {:?}",
                    nodes
                        .iter()
                        .map(|x| x.info().shape.clone())
                        .collect::<Vec<_>>()
                );
                self.spec_circuit.compiler_print();
                return Err(CircuitConstructionError::InconsistentBatches {
                    batch_shapes: vec![spec.symbol.info().shape.clone(), node.info().shape.clone()],
                    circuit: self.spec_circuit.clone(),
                });
            }
            if !spec.batchable && node.info().rank() > spec.symbol.info().rank() {
                println!(
                    "node shapes {:?}",
                    nodes
                        .iter()
                        .map(|x| x.info().shape.clone())
                        .collect::<Vec<_>>()
                );
                self.spec_circuit.compiler_print();
                return Err(CircuitConstructionError::InconsistentBatches {
                    batch_shapes: vec![spec.symbol.info().shape.clone(), node.info().shape.clone()],
                    circuit: self.spec_circuit.clone(),
                });
            }
            if !spec.expandable
                && node.info().shape[node.info().rank() - spec.symbol.info().rank()..]
                    != spec.symbol.info().shape[..]
            {
                println!(
                    "node shapes {:?}",
                    nodes
                        .iter()
                        .map(|x| x.info().shape.clone())
                        .collect::<Vec<_>>()
                );
                self.spec_circuit.compiler_print();
                return Err(CircuitConstructionError::InconsistentBatches {
                    batch_shapes: vec![spec.symbol.info().shape.clone(), node.info().shape.clone()],
                    circuit: self.spec_circuit.clone(),
                });
            }
        }
        replace_expand_bottom_up(self.spec_circuit.clone(), |c| {
            self.input_specs
                .iter()
                .position(|x| x.symbol.info().hash == c.info().hash)
                .map(|i| nodes[i].clone())
        })
    }

    pub fn expand_shape(&self, shapes: &Vec<Shape>) -> CircResult {
        if let Some(result) = MODULE_EXPANSIONS_SHAPE
            .with(|cache| cache.borrow().get(&(self.clone(), shapes.clone())).cloned())
        {
            return result;
        }
        let symbols = shapes
            .iter()
            .enumerate()
            .map(|(i, s)| {
                Symbol::nrc(
                    s.clone(),
                    ModuleNodeSpec::EXPAND_PLACEHOLDER_UUID,
                    Some(format!("{}_{:?}", i, s)),
                )
            })
            .collect();
        let result = self.expand_raw(&symbols);
        MODULE_EXPANSIONS_SHAPE.with(|cache| {
            cache
                .borrow_mut()
                .insert((self.clone(), shapes.clone()), result.clone())
        });
        result
    }

    pub fn expand(&self, nodes: &Vec<CircuitRc>) -> CircResult {
        let key: (ModuleNodeSpec, Vec<HashBytes>) =
            (self.clone(), nodes.iter().map(|x| x.info().hash).collect());
        MODULE_EXPANSIONS
            .with(|cache| cache.borrow().get(&key).cloned())
            .unwrap_or_else(|| {
                let result = (|| {
                    let shapes = nodes.iter().map(|x| x.info().shape.clone()).collect();
                    let expanded_shape = self.expand_shape(&shapes)?;
                    Ok(replace_nodes(
                        expanded_shape,
                        &nodes
                            .iter()
                            .enumerate()
                            .map(|(i, n)| {
                                (
                                    Symbol::new(
                                        n.info().shape.clone(),
                                        ModuleNodeSpec::EXPAND_PLACEHOLDER_UUID,
                                        Some(format!("{}_{:?}", i, n.info().shape)),
                                    )
                                    .info()
                                    .hash,
                                    n.clone(),
                                )
                            })
                            .collect(),
                    ))
                })();
                MODULE_EXPANSIONS.with(|cache| cache.borrow_mut().insert(key, result.clone()));
                result
            })
    }

    pub fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&self.spec_circuit.info().hash);
        for input_spec in &self.input_specs {
            hasher.update(&[input_spec.batchable as u8, input_spec.expandable as u8]);
            hasher.update(&input_spec.symbol.info().hash);
        }
        hasher.finalize().into()
    }
}
#[pymethods]
impl ModuleNodeSpec {
    #[new]
    fn new(
        spec_circuit: CircuitRc,
        input_specs: Vec<ModuleNodeArgSpec>,
        name: Option<String>,
    ) -> Self {
        Self {
            spec_circuit,
            input_specs,
            name,
        }
    }

    #[staticmethod]
    pub fn new_auto(
        circuit: CircuitRc,
        name: Option<String>,
    ) -> Result<Self, CircuitConstructionError> {
        let mut input_specs_dict: HashMap<usize, ModuleNodeArgSpec> = HashMap::new();
        let circuit = deep_map_op_context(
            circuit.clone(),
            &|sub: CircuitRc, input_specs_dict: &mut HashMap<usize, ModuleNodeArgSpec>| {
                if let Some(sym) = sub.as_symbol() {
                    static RE_NUM_BEGIN: Lazy<Regex> =
                        Lazy::new(|| Regex::new(r"#(\d+) (.*)").unwrap());
                    let captures = RE_NUM_BEGIN.captures(sym.name().unwrap()).unwrap();
                    let num = captures.get(1).unwrap().as_str().parse::<usize>().unwrap();
                    let name = captures.get(2).unwrap().as_str().to_owned();
                    let newsym = Symbol::new(sym.info().shape.clone(), sym.uuid, Some(name));
                    input_specs_dict.insert(
                        num,
                        ModuleNodeArgSpec {
                            symbol: newsym.clone(),
                            batchable: true,
                            expandable: true,
                        },
                    );
                    return Some(newsym.rc());
                }
                None
            },
            &mut input_specs_dict,
            &mut Default::default(),
        )
        .unwrap_or(circuit);
        let mut input_specs =
            vec![input_specs_dict.values().last().unwrap().clone(); input_specs_dict.len()];
        for (k, v) in input_specs_dict {
            input_specs[k] = v;
        }
        Ok(Self {
            spec_circuit: circuit,
            input_specs,
            name,
        })
    }

    #[staticmethod]
    #[args(require_all_inputs = "false")]
    pub fn new_extract(
        circuit: CircuitRc,
        input_specs: Vec<(CircuitRc, ModuleNodeArgSpec)>,
        name: Option<String>,
        require_all_inputs: bool,
    ) -> Option<Self> {
        let mut new_input_specs: Vec<Option<ModuleNodeArgSpec>> = vec![None; input_specs.len()];
        let spec_circuit = deep_map_op_context_preorder_stoppable(
            circuit,
            &|circuit,
              c: &mut (
                &mut Vec<Option<ModuleNodeArgSpec>>,
                &Vec<(CircuitRc, ModuleNodeArgSpec)>,
            )| {
                let (real_input_specs, proposed_input_specs) = c;
                if let Some(i) = proposed_input_specs
                    .iter()
                    .position(|x| x.0.info().hash == circuit.info().hash)
                {
                    let mut argspec = proposed_input_specs[i].1.clone();
                    argspec.symbol = Symbol::new(
                        circuit.info().shape.clone(),
                        argspec.symbol.uuid,
                        argspec.symbol.name_cloned().or(circuit.name_cloned()),
                    );
                    real_input_specs[i] = Some(argspec);
                    return (
                        Some(real_input_specs[i].as_ref().unwrap().symbol.clone().rc()),
                        true,
                    );
                }
                (None, false)
            },
            &mut (&mut new_input_specs, &input_specs),
            &mut Default::default(),
        )?;
        let new_input_specs: Vec<ModuleNodeArgSpec> = if require_all_inputs {
            new_input_specs.into_iter().collect::<Option<Vec<_>>>()?
        } else {
            new_input_specs
                .into_iter()
                .filter(|z| z.is_some())
                .collect::<Option<Vec<_>>>()
                .unwrap()
        };
        Some(Self {
            spec_circuit,
            input_specs: new_input_specs,
            name,
        })
    }

    pub fn resize(&self, shapes: Vec<Shape>) -> Result<Self, CircuitConstructionError> {
        let input_specs: Vec<ModuleNodeArgSpec> = zip(&self.input_specs, shapes)
            .map(|(spec, shape)| ModuleNodeArgSpec {
                symbol: Symbol::new(shape, spec.symbol.uuid, spec.symbol.name_cloned()),
                batchable: spec.batchable,
                expandable: spec.expandable,
            })
            .collect();
        let spec_circuit = replace_expand_bottom_up(self.spec_circuit.clone(), |c| {
            self.input_specs
                .iter()
                .position(|x| x.symbol.info().hash == c.info().hash)
                .map(|p| input_specs[p].symbol.clone().rc())
        })?;
        Ok(Self {
            spec_circuit,
            input_specs,
            name: self.name.clone(),
        })
    }
}

#[pyclass]
#[derive(Debug, Clone, PyClassDeriv, Hash, PartialEq, Eq)]
pub struct ModuleNodeArgSpec {
    #[pyo3(get)]
    pub symbol: Symbol,
    #[pyo3(get)]
    pub batchable: bool,
    #[pyo3(get)]
    pub expandable: bool,
}
#[pymethods]
impl ModuleNodeArgSpec {
    #[new]
    fn new(symbol: Symbol, batchable: bool, expandable: bool) -> Self {
        Self {
            symbol,
            batchable,
            expandable,
        }
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct ModuleNode {
    #[pyo3(get)]
    pub nodes: Vec<CircuitRc>,
    #[pyo3(get)]
    pub spec: ModuleNodeSpec,
    info: CachedCircuitInfo,
    #[pyo3(get)]
    name: Option<String>,
}

impl ModuleNode {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        nodes: Vec<CircuitRc>,
        spec: ModuleNodeSpec,
        name: Option<String>,
    ) -> (Result<Self, CircuitConstructionError>) {
        let shape = spec
            .expand_shape(&nodes.iter().map(|x| x.info().shape.clone()).collect())
            .map_err(|e| CircuitConstructionError::ModuleNodeExpansionError { error: Box::new(e) })?
            .info()
            .shape
            .clone();
        let mut out = Self {
            nodes,
            spec,
            name: name.clone(),
            info: Default::default(),
        };
        out.info.shape = shape;
        out.name = out.auto_name(name);

        out.init_info()
    }

    pub fn new_kwargs(
        kwargs: &HashMap<String, CircuitRc>,
        spec: ModuleNodeSpec,
        name: Option<String>,
    ) -> Result<Self, CircuitConstructionError> {
        let mut nodes: Vec<CircuitRc> = vec![spec.spec_circuit.clone(); spec.input_specs.len()];
        for (k, v) in kwargs {
            match spec
                .input_specs
                .iter()
                .position(|x| x.symbol.name().map(|n| n == k).unwrap_or(false))
            {
                Some(i) => {
                    nodes[i] = v.clone();
                }
                None => {
                    return Err(CircuitConstructionError::ModuleNodeUnknownArgument {
                        argument: k.clone(),
                    })
                }
            }
        }
        Self::try_new(nodes, spec, name)
    }
}

circuit_node_extra_impl!(ModuleNode);

impl CircuitNode for ModuleNode {
    circuit_node_auto_impl!("6825f723-f178-4dab-b568-cd85eb6d2bf3");

    fn compute_shape(&self) -> Shape {
        self.info().shape.clone()
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        for node in &self.nodes {
            hasher.update(&node.info().hash);
        }
        hasher.update(uuid!("8995f508-a7a5-4025-8d10-e46f55825cd1").as_bytes());
        hasher.update(&self.spec.compute_hash());
        hasher
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        Box::new(self.nodes.iter().cloned())
    }

    fn map_children_enumerate<F, E>(&self, mut f: F) -> Result<Self, CircuitConstructionError>
    where
        CircuitConstructionError: From<E>,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc, E>,
    {
        Self::try_new(
            self.nodes
                .iter()
                .enumerate()
                .map(move |(i, circ)| f(i, circ.clone()))
                .collect::<Result<Vec<_>, _>>()?,
            self.spec.clone(),
            self.name.clone(),
        )
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        vec![] // todo: return child axis map
    }

    fn eval_tensors(
        &self,
        _tensors: &[crate::py_types::Tensor],
        _device_dtype: &TorchDeviceDtype,
    ) -> Result<crate::py_types::Tensor, super::TensorEvalError> {
        unimplemented!();
    }
}

impl CircuitNodeAutoName for ModuleNode {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            if self.children().any(|x| x.name().is_none()) || self.spec.name.is_none() {
                None
            } else {
                Some(
                    self.spec.name.clone().unwrap()
                        + " "
                        + &self
                            .children()
                            .filter_map(|x| {
                                x.name().map(|y| {
                                    if y.len() > 100 {
                                        "...".to_owned()
                                    } else {
                                        y.to_owned()
                                    }
                                })
                            })
                            .collect::<Vec<String>>()
                            .join(" , "),
                )
            }
        })
    }
}

#[pymethods]
impl ModuleNode {
    #[cfg(feature = "real-pyo3")]
    #[new]
    #[args(spec, name, py_kwargs = "**")]
    fn new(
        spec: ModuleNodeSpec,
        name: Option<String>,
        py_kwargs: Option<&PyDict>,
    ) -> PyResult<PyClassInitializer<ModuleNode>> {
        let dict: HashMap<String, CircuitRc> = py_kwargs.unwrap().extract().unwrap();
        Ok(ModuleNode::new_kwargs(&dict, spec, name)?.into_init())
    }

    #[staticmethod]
    fn new_flat(
        nodes: Vec<CircuitRc>,
        spec: ModuleNodeSpec,
        name: Option<String>,
    ) -> Result<Self, CircuitConstructionError> {
        Self::try_new(nodes, spec, name)
    }

    pub fn expand(&self) -> CircuitRc {
        self.spec
            .expand(&self.nodes)
            .map_err(|e| CircuitConstructionError::ModuleNodeExpansionError { error: Box::new(e) })
            .unwrap()
    }
}

#[pyfunction]
pub fn inline_all_modules(circuit: CircuitRc) -> CircuitRc {
    deep_map_unwrap(circuit, |c| match &**c {
        Circuit::ModuleNode(mn) => inline_all_modules(mn.expand()),
        _ => c.clone(),
    })
}
use std::cell::RefCell;
thread_local! {
    static MODULE_EXPANSIONS: RefCell<HashMap<(ModuleNodeSpec, Vec<HashBytes>), CircResult>> =
        RefCell::new(HashMap::new());
    static MODULE_EXPANSIONS_SHAPE: RefCell<HashMap<(ModuleNodeSpec, Vec<Shape>), CircResult>> =
        RefCell::new(HashMap::new());
}
