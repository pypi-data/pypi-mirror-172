use super::{
    deep_map, deep_map_op_context_preorder_stoppable, deep_map_preorder, deep_map_unwrap_preorder,
    prelude::*, visit_circuit, visit_circuit_fallable, HashBytes,
};
use crate::hashmaps::{AHashSet as HashSet, FxHashMap as HashMap};
use crate::pycall;
use pyo3::{pyfunction, PyObject, Python};

pub fn filter_nodes(circuit: CircuitRc, filter: &dyn Fn(CircuitRc) -> bool) -> HashSet<CircuitRc> {
    let mut result: HashSet<CircuitRc> = HashSet::new();
    visit_circuit(circuit, |circuit| {
        if filter(circuit.clone()) {
            result.insert(circuit);
        }
    });
    result
}

#[pyfunction]
#[pyo3(name = "filter_nodes")]
pub fn filter_nodes_py(
    circuit: CircuitRc,
    filter: PyObject,
) -> Result<HashSet<CircuitRc>, CircuitConstructionError> {
    let mut result: HashSet<CircuitRc> = HashSet::new();
    let err = visit_circuit_fallable(circuit, |circuit| {
        let filter_result: Result<_, CircuitConstructionError> =
            pycall!(filter, (circuit.clone(),), CircuitConstructionError);
        let filter_result = filter_result?;
        if filter_result {
            result.insert(circuit);
        }
        Ok(())
    });
    err.map(|_x| result)
}

#[pyfunction]
#[pyo3(name = "replace_nodes")]
pub fn replace_nodes_py(circuit: CircuitRc, map: HashMap<CircuitRc, CircuitRc>) -> CircuitRc {
    deep_map_unwrap_preorder(circuit, |x: CircuitRc| -> CircuitRc {
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
#[pyo3(name = "deep_map_preorder")]
pub fn deep_map_preorder_py(
    circuit: CircuitRc,
    f: PyObject,
) -> Result<CircuitRc, CircuitConstructionError> {
    deep_map_preorder(
        circuit,
        |x: CircuitRc| -> Result<CircuitRc, CircuitConstructionError> {
            pycall!(f, (x,), CircuitConstructionError)
        },
    )
}

#[pyfunction]
#[pyo3(name = "deep_map")]
pub fn deep_map_py(circuit: CircuitRc, f: PyObject) -> Result<CircuitRc, CircuitConstructionError> {
    deep_map(circuit, &|x: CircuitRc| -> Result<
        CircuitRc,
        CircuitConstructionError,
    > {
        pycall!(f, (x,), CircuitConstructionError)
    })
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
