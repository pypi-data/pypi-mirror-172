use super::{
    deep_map_op_context_preorder_stoppable, deep_map_preorder, deep_map_preorder_unwrap,
    prelude::*, visit_circuit, HashBytes,
};
use crate::hashmaps::{AHashSet as HashSet, FxHashMap as HashMap};
use crate::{pycall, pycallable};
use macro_rules_attribute::apply;
use pyo3::{pyfunction, PyObject, Python};

#[apply(pycallable)]
#[pyo3(name = "filter_nodes")]
pub fn filter_nodes<F>(
    circuit: CircuitRc,
    filter: F,
) -> Result<HashSet<CircuitRc>, CircuitConstructionError>
where
    F: Fn((circuit, CircuitRc)) -> Result<bool, _>,
{
    let mut result: HashSet<CircuitRc> = HashSet::new();
    visit_circuit(circuit, |circuit: CircuitRc| {
        if filter(circuit.clone())? {
            result.insert(circuit);
        }
        Ok(())
    })?;
    Ok(result)
}

#[pyfunction]
#[pyo3(name = "replace_nodes")]
pub fn replace_nodes_py(circuit: CircuitRc, map: HashMap<CircuitRc, CircuitRc>) -> CircuitRc {
    deep_map_preorder_unwrap(circuit, |x: CircuitRc| -> CircuitRc {
        map.get(&x).cloned().unwrap_or(x)
    })
}

/// Replaces child nodes recursively with a mapping
/// In pre-order so that high level nodes are replaced first
pub fn replace_nodes(circuit: CircuitRc, map: &HashMap<HashBytes, CircuitRc>) -> CircuitRc {
    deep_map_op_context_preorder_stoppable(
        circuit.clone(),
        &|x: CircuitRc, _| {
            let rc = x;
            let result = map.get(&rc.info().hash).cloned();
            let stop = result.is_some();
            (result, stop)
        },
        &mut (),
        &mut Default::default(),
    )
    .unwrap_or(circuit)
}

#[pyfunction]
#[pyo3(name = "update_nodes")]
pub fn update_nodes_py(
    circuit: CircuitRc,
    matcher: PyObject,
    updater: PyObject,
) -> Result<CircuitRc, CircuitConstructionError> {
    let nodes = filter_nodes_py(circuit.clone(), matcher)?;
    deep_map_preorder(circuit, |x| {
        if nodes.contains(&x) {
            pycall!(updater, (x,), CircuitConstructionError)
        } else {
            Ok(x)
        }
    })
}

pub type CircuitPath = Vec<usize>;

#[pyfunction]
pub fn path_get(circuit: CircuitRc, path: CircuitPath) -> Option<CircuitRc> {
    let mut cur = circuit;
    for i in path {
        let children: Vec<CircuitRc> = cur.children().collect();
        if i >= children.len() {
            return None;
        }
        cur = children[i].clone()
    }
    Some(cur)
}

pub fn update_path<F>(
    circuit: CircuitRc,
    path: &CircuitPath,
    updater: F,
) -> Result<CircuitRc, CircuitConstructionError>
where
    F: Fn(CircuitRc) -> Result<CircuitRc, CircuitConstructionError>,
{
    fn recurse<F>(
        circuit: CircuitRc,
        path: &CircuitPath,
        path_idx: usize,
        updater: &F,
    ) -> Result<CircuitRc, CircuitConstructionError>
    where
        F: Fn(CircuitRc) -> Result<CircuitRc, CircuitConstructionError>,
    {
        if path_idx == path.len() {
            return updater(circuit);
        }
        circuit
            .map_children_enumerate(|i, circuit| {
                if i == path[path_idx] {
                    recurse(circuit, path, path_idx + 1, updater)
                } else {
                    Ok(circuit)
                }
            })
            .map(|z| z.rc())
    }
    recurse(circuit, path, 0, &updater)
}

#[pyfunction]
#[pyo3(name = "update_path")]
pub fn update_path_py(
    circuit: CircuitRc,
    path: CircuitPath,
    updater: PyObject,
) -> Result<CircuitRc, CircuitConstructionError> {
    update_path(circuit, &path, |x| {
        pycall!(updater, (x.clone(),), CircuitConstructionError)
    })
}
