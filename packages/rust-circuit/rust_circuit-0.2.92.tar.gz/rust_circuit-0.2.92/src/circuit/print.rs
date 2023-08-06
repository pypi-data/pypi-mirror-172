use crate::hashmaps::FxHashMap as HashMap;

use super::{
    circuit_utils::{count_nodes, toposort_circuit, total_flops},
    prelude::*,
    repr::ReprWrapper,
    repr::{repr_op_string, RustRepr},
    HashBytes,
};

use num_bigint::BigUint;
use pyo3::pyfunction;

pub fn repr_circuit_deep_compiler(
    circuit: &Circuit,
    bijection: bool,
    shape_only_necessesary: bool,
) -> String {
    let mut seen_hashes: HashMap<HashBytes, String> = HashMap::new();
    fn recurse(
        circ: &Circuit,
        depth: usize,
        result: &mut String,
        seen_hashes: &mut HashMap<HashBytes, String>,
        bijection: bool,
        shape_only_necessary: bool,
    ) {
        result.push_str(&" ".repeat(depth * 2));
        if let Some(prev) = seen_hashes.get(&circ.info().hash) {
            result.push_str(prev);
            result.push('\n');
            return;
        }
        let variant_string = circ.variant_string();
        let variant_string_simplified = variant_string
            .strip_suffix("Constant")
            .unwrap_or(&variant_string);
        seen_hashes.insert(
            circ.info().hash,
            seen_hashes.len().to_string() + " " + circ.name().unwrap_or(variant_string_simplified),
        );
        result.push_str(&(seen_hashes.len() - 1).to_string());
        if let Some(n) = circ.name() {
            result.push(' ');
            if bijection {
                result.push('\'');
                result.push_str(&n.replace('\\', r"\\").replace('\'', r"\'"));
                result.push('\'');
            } else {
                result.push_str(n);
            }
        }
        if !shape_only_necessary
            || matches!(
                circ,
                Circuit::ScalarConstant(_)
                    | Circuit::Scatter(_)
                    | Circuit::Symbol(_)
                    | Circuit::ArrayConstant(_)
            )
        {
            result.push_str(&format!(" {:?}", circ.info().shape));
        }
        result.push(' ');
        if !bijection
            && circ.info().numel() > BigUint::from(400_000_000usize)
            && !matches!(circ, Circuit::ArrayConstant(_))
        {
            result.push_str(&format!(
                "\u{001b}[31m{}\u{001b}[0m ",
                oom_fmt(circ.info().numel())
            ));
        }
        result.push_str(variant_string_simplified);
        result.push(' ');
        result.push_str(&{
            match circ {
                Circuit::ScalarConstant(scalar) => {
                    format!("{:.}", scalar.value)
                }
                Circuit::Rearrange(rearrange) => rearrange.spec.to_einops_string(true),
                Circuit::Einsum(einsum) => einsum.get_spec().to_einsum_string(),
                Circuit::Index(index) => {
                    if bijection {
                        index.index.repr_bijection()
                    } else {
                        format!("{}", index.index)
                    }
                }
                Circuit::Scatter(scatter) => {
                    if bijection {
                        scatter.index.repr_bijection()
                    } else {
                        format!("{}", scatter.index)
                    }
                }
                Circuit::Concat(concat) => concat.axis.to_string(),
                Circuit::GeneralFunction(gf) => gf.spec.name.clone(),
                Circuit::Symbol(sy) => {
                    if sy.uuid.is_nil() {
                        "".to_owned()
                    } else {
                        format!("{}", &sy.uuid)
                    }
                }
                Circuit::ModuleNode(mn) => {
                    (&mn.spec.name.as_ref().unwrap_or(&"".to_owned())).to_string()
                }
                Circuit::ArrayConstant(ac) => {
                    if bijection {
                        ac.save_rrfs().unwrap();
                        ac.tensor_hash_base16()[..14].to_owned()
                    } else {
                        "".to_owned()
                    }
                }
                Circuit::AutoTag(at) => at.uuid.to_string(),
                Circuit::StoredCumulantVar(scv) => {
                    format!(
                        "{}|{}",
                        scv.cumulants
                            .keys()
                            .map(|k| k.to_string())
                            .collect::<Vec<_>>()
                            .join(", "),
                        scv.uuid.to_string(),
                    )
                }
                _ => "".to_owned(),
            }
        });
        if !circ.info().named_axes.is_empty() {
            result.push_str(&format!(
                " NA[{}]",
                (0..circ.info().rank())
                    .map(|x| match circ.info().named_axes.get(&(x as u8)) {
                        None => "".to_owned(),
                        Some(s) => s.clone(),
                    })
                    .collect::<Vec<_>>()
                    .join(",")
            ))
        }
        result.push('\n');
        for child in circ.children() {
            recurse(
                &child,
                depth + 1,
                result,
                seen_hashes,
                bijection,
                shape_only_necessary,
            );
        }
    }
    let mut result = String::new();
    recurse(
        circuit,
        0,
        &mut result,
        &mut seen_hashes,
        bijection,
        shape_only_necessesary,
    );
    result
}

pub fn oom_fmt<T: Into<BigUint>>(num: T) -> String {
    let mut num: BigUint = num.into();
    let k = BigUint::from(1000usize);
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"].iter() {
        if &num < &k {
            return format!("{}{}", num, unit);
        }
        num /= &k;
    }
    format!("{}Y", num)
}

pub fn print_circuit_stats(circuit: &Circuit) {
    let mut result = String::new();
    result.push_str(
        &circuit
            .name_cloned()
            .map(|x| x + " ")
            .unwrap_or(" ".to_owned()),
    );
    result.push_str(&circuit.variant_string());
    result.push_str(&format!(
        " nodes {} max_size {} flops {}",
        count_nodes(circuit.clone().rc()),
        oom_fmt(circuit.max_non_input_size()),
        oom_fmt(total_flops(circuit.clone().rc()))
    ));
    println!("{}", result);
}
