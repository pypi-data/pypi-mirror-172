use crate::hashmaps::{AHashSet as HashSet, FxHashMap as HashMap};
use crate::util::is_unique;
use std::collections::BTreeMap;

use uuid::Uuid;

use super::circuit_utils::deep_map_pass_down_branching;
use super::{deep_map_unwrap, prelude::*, visit_circuit_with_parents_fallible, NamedAxes};

use crate::pyo3_prelude::*;

pub fn set_named_axes<T: CircuitNode>(node: T, named_axes: NamedAxes) -> T {
    node.update_info(|i| i.named_axes = named_axes).unwrap()
}

#[pyfunction]
#[pyo3(name = "set_named_axes")]
pub fn set_named_axes_py(circuit: CircuitRc, named_axes: NamedAxes) -> CircuitRc {
    set_named_axes(circuit, named_axes)
}
pub fn merge_named_axes(a: &NamedAxes, b: &NamedAxes) -> NamedAxes {
    let mut result = a.clone();
    result.extend(b.clone().into_iter());
    result
}

pub fn named_axes_backward<T: CircuitNode + Clone>(
    circuit: &T,
    named_axes: &NamedAxes,
) -> Vec<NamedAxes> {
    let child_axis_map = circuit.child_axis_map();
    child_axis_map
        .iter()
        .map(|z| {
            z.iter()
                .enumerate()
                .filter_map(|(child_i, ax)| {
                    ax.and_then(|i| {
                        named_axes
                            .get(&(i as u8))
                            .map(|name| (child_i as u8, name.clone()))
                    })
                })
                .collect()
        })
        .collect()
}

#[pyfunction]
pub fn propagate_named_axes(
    circuit: CircuitRc,
    named_axes: NamedAxes,
    abort_on_branch: bool,
) -> CircuitRc {
    deep_map_pass_down_branching(
        circuit,
        |circuit, axes| {
            let child_axis_names: Vec<NamedAxes> = if abort_on_branch
                && circuit
                    .as_einsum()
                    .map(|x| x.args.iter().any(|(_, i)| !is_unique(i)))
                    .unwrap_or(false)
            {
                circuit
                    .children()
                    .map(|_c| Default::default())
                    .collect::<Vec<NamedAxes>>()
            } else {
                named_axes_backward(&**circuit, &{ axes.clone() })
            };
            child_axis_names
        },
        |circuit, named_axes, children| {
            set_named_axes(
                circuit.map_children_unwrap_idxs(|i| children[i].clone()),
                merge_named_axes(&circuit.info().named_axes, named_axes),
            )
            .rc()
        },
        named_axes,
    )
}

pub fn axis_of_name(circuit: &Circuit, name: &str) -> Option<usize> {
    circuit
        .info()
        .named_axes
        .iter()
        .find(|(_i, s)| *s == name)
        .map(|(i, _s)| *i as usize)
}

#[pyfunction]
/// returns tuple (leavs with axis, leavs without axis)
pub fn get_axis_leaves(
    circuit: CircuitRc,
    axis: usize,
    _error_on_removable_axis_leaf: bool,
) -> Result<
    (
        String,
        CircuitRc,
        HashMap<CircuitRc, usize>,
        HashSet<CircuitRc>,
    ),
    CircuitConstructionError,
> {
    let name = Uuid::new_v4().to_string();
    if circuit
        .as_einsum()
        .map(|x| {
            x.out_axes
                .iter()
                .filter(|i| x.out_axes[axis] == **i)
                .count()
                != 1
        })
        .unwrap_or(false)
    {
        return Ok((
            name,
            circuit.clone(),
            HashMap::from([(circuit, axis)]),
            HashSet::new(),
        ));
    }
    let circ_named_axes =
        propagate_named_axes(circuit, BTreeMap::from([(axis as u8, name.clone())]), true);
    // circ_named_axes.compiler_print();
    let mut result_axis: HashMap<CircuitRc, usize> = Default::default();
    let mut result_no_axis: HashSet<CircuitRc> = Default::default();
    let _names_to_remove = Some(HashSet::from([name.clone()]));
    visit_circuit_with_parents_fallible(circ_named_axes.clone(), |x, parents| {
        // println!("child");
        // x.compiler_print();
        // println!("parents");
        // for parent in parents {
        //     parent.compiler_print();
        // }
        if let Some(i) = axis_of_name(&x,&name) && !x.children().any(|child|axis_of_name(&child, &name).is_some())
        {
            // if  error_on_removable_axis_leaf && get_removable_axes(&x.clone().rc()).contains(&i){
            //     return Err(CircuitConstructionError::ExpandingRemovableAxisUnfortunateError {  })
            // }
            result_axis.insert(x.clone(), i);
        }

        if axis_of_name(&x, &name).is_none()
            && parents
                .iter()
                .any(|child| axis_of_name(child, &name).is_some())
        {
            result_no_axis.insert(x);
        }
        Ok::<(), CircuitConstructionError>(())
    })?;
    Ok((name, circ_named_axes, result_axis, result_no_axis))
}

/// remove all instances of this axis name from circuit
pub fn deep_strip_axis_names(circuit: CircuitRc, names: &Option<HashSet<String>>) -> CircuitRc {
    deep_map_unwrap(circuit, |x| {
        let axis_names: NamedAxes = if let Some(blacklist) = &names {
            x.info()
                .named_axes
                .clone()
                .into_iter()
                .filter(|(_i, name)| !blacklist.contains(name))
                .collect()
        } else {
            BTreeMap::new()
        };
        set_named_axes(x, axis_names)
    })
}
