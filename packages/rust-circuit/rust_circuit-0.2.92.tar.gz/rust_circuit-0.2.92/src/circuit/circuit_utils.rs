use std::{collections::BTreeSet, iter::zip};

use crate::hashmaps::{AHashSet as HashSet, FxHashMap as HashMap};

use crate::{
    opt_einsum::EinsumSpec,
    pyo3_prelude::*,
    tensor_util::{TensorAxisIndex, TensorIndex},
};
use num_bigint::BigUint;

use super::{
    apply_fn_cache, deep_map_op_pre_new_children, deep_map_unwrap, visit_circuit_unwrap,
    ArrayConstant, Circuit, CircuitNode, CircuitRc, HashBytes, Index,
};
use crate::tensor_util::TorchDeviceDtype;
use std::hash::Hash;

#[pyfunction]
pub fn cast_circuit(circ: CircuitRc, device_dtype: &TorchDeviceDtype) -> CircuitRc {
    deep_map_op_pre_new_children(
        circ.clone(),
        |circ, children: &Vec<CircuitRc>| match &**circ {
            Circuit::ArrayConstant(node) => {
                if &TorchDeviceDtype::from_tensor(&node.value) != device_dtype {
                    Some(ArrayConstant::nrc(
                        device_dtype.cast_tensor(node.value.clone()),
                        node.name_cloned(),
                    ))
                } else {
                    None
                }
            }
            Circuit::Index(node) => {
                if node
                    .index
                    .0
                    .iter()
                    .any(|x| matches!(x, TensorAxisIndex::Tensor(_)))
                {
                    Some(Index::nrc(
                        children[0].clone(),
                        TensorIndex(
                            node.index
                                .0
                                .iter()
                                .map(|idx| match idx {
                                    TensorAxisIndex::Tensor(tensor) => TensorAxisIndex::Tensor(
                                        TorchDeviceDtype {
                                            device: device_dtype.device.clone(),
                                            dtype: "int64".to_owned(),
                                        }
                                        .cast_tensor(tensor.clone()),
                                    ),
                                    _ => idx.clone(),
                                })
                                .collect(),
                        ),
                        node.name_cloned(),
                    ))
                } else {
                    None
                }
            }
            _ => None,
        },
    )
    .unwrap_or(circ)
}

#[pyfunction]
pub fn count_nodes(circuit: CircuitRc) -> usize {
    let mut result: usize = 0;
    visit_circuit_unwrap(circuit, &mut |_x: CircuitRc| {
        result += 1;
    });
    result
}

pub fn hash_to_node(circuit: CircuitRc) -> HashMap<HashBytes, CircuitRc> {
    let mut result: HashMap<HashBytes, CircuitRc> = HashMap::new();
    visit_circuit_unwrap(circuit, &mut |x: CircuitRc| {
        result.insert(x.info().hash, x.clone());
    });
    result
}

pub fn subcircuits(circuit: CircuitRc) -> HashSet<CircuitRc> {
    let mut result: HashSet<CircuitRc> = HashSet::new();
    visit_circuit_unwrap(circuit, &mut |x: CircuitRc| {
        result.insert(x);
    });
    result
}

#[pyfunction]
pub fn total_flops(circuit: CircuitRc) -> BigUint {
    let mut result: BigUint = BigUint::from(0usize);
    visit_circuit_unwrap(circuit, &mut |x: CircuitRc| {
        result += x.self_flops();
    });
    result
}

pub fn total_flops_cached(circuit: CircuitRc, cache: &mut HashMap<HashBytes, BigUint>) -> BigUint {
    apply_fn_cache(
        &circuit,
        |x| total_flops(x.clone()),
        cache,
        |x| x.info().hash,
    )
}

#[pyfunction]
pub fn total_arrayconstant_size(circuit: CircuitRc) -> BigUint {
    let mut result: BigUint = BigUint::from(0usize);
    visit_circuit_unwrap(circuit, &mut |x: CircuitRc| {
        if let Circuit::ArrayConstant(x) = &**x {
            result += x.info().numel();
        }
    });
    result
}

#[pyfunction]
pub fn sum_of_node_sizes(circuit: CircuitRc) -> BigUint {
    let mut result: BigUint = BigUint::from(0usize);
    visit_circuit_unwrap(circuit, &mut |x: CircuitRc| {
        if !matches!(&**x, Circuit::ArrayConstant(_)) {
            result += x.info().numel();
        }
    });
    result
}

pub fn sum_of_node_sizes_cached(
    circuit: CircuitRc,
    cache: &mut HashMap<HashBytes, BigUint>,
) -> BigUint {
    apply_fn_cache(
        &circuit,
        |x| sum_of_node_sizes(x.clone()),
        cache,
        |x| x.info().hash,
    )
}

#[pyfunction]
pub fn get_leaves(circuit: CircuitRc) -> Vec<CircuitRc> {
    let mut result: Vec<CircuitRc> = vec![];
    visit_circuit_unwrap(circuit, &mut |c: CircuitRc| {
        if c.children().count() == 0 {
            result.push(c);
        }
    });
    result
}

#[pyfunction]
pub fn get_all_einsum_specs(circuit: CircuitRc) -> Vec<EinsumSpec> {
    let mut result: Vec<EinsumSpec> = vec![];
    visit_circuit_unwrap(circuit, |c| {
        if let Circuit::Einsum(node) = &**c {
            result.push(node.get_spec());
        }
    });
    result
}

#[pyfunction]
/// children first
pub fn toposort_circuit(circuit: CircuitRc) -> Vec<CircuitRc> {
    let mut num_refs: HashMap<CircuitRc, usize> = HashMap::new();
    visit_circuit_unwrap(circuit.clone(), |c| {
        for child in c.children() {
            *num_refs.entry(child).or_insert(0) += 1;
        }
    });
    let mut ready: BTreeSet<CircuitRc> = BTreeSet::from([circuit]);
    let mut result: Vec<CircuitRc> = vec![];
    while !ready.is_empty() {
        let here = ready.pop_first().unwrap();
        for child in here.children() {
            num_refs.insert(child.clone(), num_refs[&child] - 1);
            if num_refs[&child] == 0 {
                ready.insert(child);
            }
        }
        result.push(here.clone())
    }
    result.reverse();
    result
}

pub fn deep_map_pass_up<F, T>(circuit: CircuitRc, mut f: F) -> (CircuitRc, T)
where
    T: Clone,
    F: FnMut(CircuitRc, Vec<T>) -> (CircuitRc, T),
{
    let topo = toposort_circuit(circuit.clone());
    let mut pass_ups: HashMap<CircuitRc, T> = HashMap::new();
    for c in topo {
        let passed_up = c.children().map(|c| pass_ups[&c].clone()).collect();
        let (new, pass_here) = f(c.clone(), passed_up);
        pass_ups.insert(c.clone(), pass_here.clone());
        if c == circuit {
            return (new, pass_here);
        }
    }
    panic!();
}

pub fn deep_map_pass_down<F, F2, T>(circuit: CircuitRc, pass_down: F, make_circuit: F2) -> CircuitRc
where
    F: Fn(CircuitRc, &Vec<T>) -> Vec<T>,
    F2: Fn(CircuitRc, &Vec<T>) -> CircuitRc,
{
    let mut toposorted = toposort_circuit(circuit.clone());
    toposorted.reverse();
    let mut passed_down: HashMap<CircuitRc, Vec<T>> = HashMap::new();
    for c in toposorted {
        let pass = pass_down(c.clone(), passed_down.get(&c).unwrap_or(&vec![]));
        for (child, pass) in zip(c.children(), pass) {
            passed_down
                .entry(child.clone())
                .or_insert(vec![])
                .push(pass);
        }
    }
    deep_map_unwrap(circuit, |c| {
        make_circuit(c.clone(), passed_down.get(&c).unwrap_or(&vec![]))
    })
}

pub fn deep_map_pass_down_branching<F, F2, T>(
    circuit: CircuitRc,
    pass_down_f: F,
    make_circuit_f: F2,
    initial_pass_down: T,
) -> CircuitRc
where
    T: Hash + Eq + Clone,
    F: Fn(CircuitRc, &T) -> Vec<T>,
    F2: Fn(CircuitRc, &T, &Vec<CircuitRc>) -> CircuitRc,
{
    let mut pass_down_cache: HashMap<(CircuitRc, T), Vec<T>> = HashMap::new();
    let mut construct_cache: HashMap<(CircuitRc, T), CircuitRc> = HashMap::new();

    fn recurse<F, F2, T>(
        circuit: CircuitRc,
        passed: T,
        pdf: &F,
        mcf: &F2,
        pdc: &mut HashMap<(CircuitRc, T), Vec<T>>,
        cc: &mut HashMap<(CircuitRc, T), CircuitRc>,
    ) -> CircuitRc
    where
        T: Hash + Eq + Clone,
        F: Fn(CircuitRc, &T) -> Vec<T>,
        F2: Fn(CircuitRc, &T, &Vec<CircuitRc>) -> CircuitRc,
    {
        let pass_key = (circuit.clone(), passed.clone());
        if let Some(result) = cc.get(&pass_key) {
            return result.clone();
        }
        let passing = pdc.get(&pass_key).cloned().unwrap_or_else(|| {
            let result = pdf(circuit.clone(), &passed);
            pdc.insert(pass_key.clone(), result.clone());
            result
        });
        let new_children: Vec<CircuitRc> = zip(circuit.children(), passing)
            .map(|(child, pass)| recurse(child, pass, pdf, mcf, pdc, cc))
            .collect();

        let result = mcf(circuit, &passed, &new_children);
        cc.insert(pass_key, result.clone());
        result
    }
    recurse(
        circuit,
        initial_pass_down,
        &pass_down_f,
        &make_circuit_f,
        &mut pass_down_cache,
        &mut construct_cache,
    )
}

#[pyfunction]
pub fn replace_all_randn_seeded(circuit: CircuitRc) -> CircuitRc {
    deep_map_unwrap(circuit, |node| match &**node {
        Circuit::ArrayConstant(ac) => ArrayConstant::randn_seeded(
            ac.info().shape.clone(),
            ac.name_cloned(),
            ac.info().device_dtype.clone(),
            // We use the tensor hash instead of the circuit hash
            ac.value.hash_usize().unwrap(),
        )
        .rc(),
        Circuit::Index(index) => Index::nrc(
            index.node.clone(),
            TensorIndex(
                zip(&index.index.0, &index.node.info().shape)
                    .map(|(i, l)| {
                        if let TensorAxisIndex::Tensor(t) = i {
                            return TensorAxisIndex::new_tensor_randint_seeded(
                                t.shape()[0],
                                *l,
                                index.info().device_dtype.clone(),
                                t.hash_usize().unwrap(),
                            );
                        }
                        i.clone()
                    })
                    .collect(),
            ),
            index.name_cloned(),
        ),
        _ => node.clone(),
    })
}

pub fn has_leaf_symbols(circuit: CircuitRc, allowed: &HashSet<HashBytes>) -> bool {
    let mut result = false;
    super::visit_circuit_unwrap(circuit, |circuit| {
        if circuit.as_symbol().is_some() && !allowed.contains(&circuit.info().hash) {
            println!(
                "found symbol {:?} allowed {:?}",
                circuit.info().hash,
                allowed
            );
            result = true;
        }
        if let Circuit::ModuleNode(mn) = &**circuit {
            let inner_allowed: HashSet<HashBytes> = allowed
                .iter()
                .cloned()
                .chain(mn.spec.input_specs.iter().map(|s| s.symbol.info().hash))
                .collect();
            result = result || has_leaf_symbols(mn.spec.spec_circuit.clone(), &inner_allowed);
        }
    });
    result
}
