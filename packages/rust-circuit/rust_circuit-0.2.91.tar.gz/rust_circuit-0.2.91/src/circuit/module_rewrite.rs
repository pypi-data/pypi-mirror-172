use crate::{circuit::ModuleNode, pyo3_prelude::*};

use super::{circuit_utils::count_nodes, CircuitRc};
#[pyfunction]
pub fn elim_empty_module(circuit: &ModuleNode) -> Option<CircuitRc> {
    if count_nodes(circuit.spec.spec_circuit.clone()) == 1 {
        return Some(circuit.nodes[0].clone());
    }
    return None;
}
