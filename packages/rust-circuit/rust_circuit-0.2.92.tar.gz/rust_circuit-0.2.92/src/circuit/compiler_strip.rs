use super::circuit_optimizer::OptimizationContext;
use super::{deep_map_op_context, Circuit, CircuitNode, CircuitRc};

use crate::pyo3_prelude::*;

/// don't change symbols bc their names matter for correctness
#[pyfunction]
#[pyo3(name = "strip_names")]
pub fn strip_names_py(circuit: CircuitRc) -> CircuitRc {
    strip_names(circuit, &mut Default::default())
}
pub fn strip_names(circuit: CircuitRc, context: &mut OptimizationContext) -> CircuitRc {
    deep_map_op_context(
        circuit.clone(),
        &|circuit, _| match &**circuit {
            Circuit::Symbol(_sym) => None,
            _ => circuit
                .name()
                .map(|_| (**circuit).clone().rename(None).rc()),
        },
        &mut (),
        &mut context.cache.stripped_names,
    )
    .unwrap_or(circuit)
}
