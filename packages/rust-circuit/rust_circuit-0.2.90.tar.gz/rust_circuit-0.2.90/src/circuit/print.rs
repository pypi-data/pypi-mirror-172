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

/// gets a Rust expression that will evaluate to the circuit, assuming children are already constructed.
/// context maps children to variable names.
/// we use a top sort to determine to order of calls to this function so that
/// context always has the names for circuits we'll need to repr this one
pub fn repr_circuit_one_level(
    circuit: &CircuitRc,
    context: &HashMap<CircuitRc, String>,
    tensors_as_randn: bool,
) -> String {
    let node_string = |x: &CircuitRc| format!("{}.clone()", context[x]);
    match circuit.as_ref() {
        Circuit::Einsum(e) => {
            let einargs = e
                .args
                .iter()
                .map(|(c, ax)| ReprWrapper(format!("({}, {})", node_string(c), ax.repr())))
                .collect::<Vec<ReprWrapper>>()
                .repr();
            format!(
                "Einsum::nrc({}, {}, {})",
                einargs,
                e.out_axes.repr(),
                repr_op_string(&e.name_cloned())
            )
        }
        Circuit::ArrayConstant(a) => {
            if tensors_as_randn {
                format!(
                    "ArrayConstant::randn_seeded({}, {}, {}, {}).rc()",
                    a.info().shape.repr(),
                    repr_op_string(&a.name_cloned()),
                    a.info().device_dtype.repr(),
                    a.value.hash_usize().unwrap(),
                )
            } else {
                let hash_base16 = a.save_rrfs().unwrap();
                format!(
                    "ArrayConstant::from_hash({},{}).unwrap().rc()",
                    repr_op_string(&a.name_cloned()),
                    (&hash_base16 as &str).repr(),
                )
            }
        }
        Circuit::Symbol(s) => format!(
            "Symbol::nrc({}, {}, {})",
            s.info().shape.repr(),
            s.uuid.repr(),
            repr_op_string(&s.name_cloned())
        ),
        Circuit::ScalarConstant(s) => format!(
            "ScalarConstant::nrc({}, {}, {})",
            s.value.repr(),
            s.info().shape.repr(),
            repr_op_string(&s.name_cloned())
        ),
        Circuit::Add(a) => {
            let variable_names: Vec<String> = a.children().map(|c| node_string(&c)).collect();
            format!(
                "Add::nrc(vec![{}], {})",
                variable_names.join(", "),
                repr_op_string(&a.name_cloned())
            )
        }
        Circuit::Rearrange(r) => {
            format!(
                "Rearrange::nrc({}, {}, {})",
                node_string(&r.node),
                r.spec.repr(),
                repr_op_string(&r.name_cloned())
            )
        }
        Circuit::Index(i) => format!(
            "Index::nrc({}, {}, {})",
            node_string(&i.node),
            i.index.repr(
                i.node.info().shape.clone(),
                &i.info().device_dtype,
                tensors_as_randn
            ),
            repr_op_string(&i.name_cloned())
        ),
        Circuit::GeneralFunction(g) => {
            if g.spec.is_official {
                let variable_names: Vec<String> = g.children().map(|x| node_string(&x)).collect();
                format!(
                    "GeneralFunction::new_by_name(vec![{}], {}, {}).unwrap().rc()",
                    variable_names.join(", "),
                    g.spec.name.repr(),
                    repr_op_string(&g.name_cloned())
                )
            } else {
                panic!(
                    "cant print non-official generalfunctions {} {:?}",
                    g.spec.name, g.spec.function
                );
            }
        }
        Circuit::Concat(c) => {
            let variable_names: Vec<String> = c.children().map(|x| node_string(&x)).collect();
            format!(
                "Concat::nrc(vec![{}], {}, {})",
                variable_names.join(", "),
                c.axis,
                repr_op_string(&c.name_cloned())
            )
        }
        Circuit::Scatter(s) => {
            format!(
                "Scatter::nrc({}, {}, {}, {})",
                node_string(&s.node),
                // indices are into the output zero-padded array, so we use the shape of s instead of s.node
                s.index.repr(
                    s.info().shape.clone(),
                    &s.info().device_dtype,
                    tensors_as_randn
                ),
                s.info().shape.repr(),
                repr_op_string(&s.name_cloned())
            )
        }
        Circuit::ModuleNode(mn) => {
            format!(
                "ModuleNode::nrc(vec![{}],{},{})",
                mn.children()
                    .map(|x| node_string(&x))
                    .collect::<Vec<_>>()
                    .join(", "),
                mn.spec.repr(),
                repr_op_string(&mn.name_cloned())
            )
        }
        Circuit::AutoTag(at) => format!(
            "AutoTag::nrc({}, {}, {})",
            node_string(&at.node),
            at.uuid.repr(),
            repr_op_string(&at.name_cloned())
        ),
        Circuit::DiscreteVar(dv) => format!(
            "DiscreteVar::nrc({},{},{})",
            node_string(&dv.values),
            node_string(&dv.probs_and_group),
            repr_op_string(&dv.name_cloned())
        ),
        Circuit::StoredCumulantVar(scv) => format!(
            "StoredCumulantVar::nrc(BTreeMap::from([{}]),{},{})",
            scv.cumulants
                .iter()
                .map(|(k, v)| format!("({},{})", k.to_string(), node_string(&v)))
                .collect::<Vec<_>>()
                .join(","),
            scv.uuid.repr(),
            repr_op_string(&scv.name_cloned())
        ),
        Circuit::Cumulant(cum) => format!(
            "Cumulant::nrc(vec![{}],{})",
            cum.nodes
                .iter()
                .map(|v| node_string(&v))
                .collect::<Vec<_>>()
                .join(","),
            repr_op_string(&cum.name_cloned())
        ),
    }
}

/// Prints out a string of Rust code representing an expression that evaluates to something similar
/// to circuit provided. Currently it ablates array constants and int tensors for tensor indexing
/// with seeded randn tensors, so the evaluation may be different. This transformation is not invariant
/// to some rewrites as a result.
///
/// There's an analogous Python function, interp.circuit.print_circuit.lambda_notation_circuit
///
/// Python example:
/// >>> import rust_circuit
/// >>> a = rust_circuit.ScalarConstant(0.2, (3,), 'a')
/// >>> b = rust_circuit.ScalarConstant(0.5, (3,))
/// >>> s = rust_circuit.Add([a, b], 's')
/// >>> q = rust_circuit.Concat([a, s], 0, 'cat')
/// >>> print(rust_circuit.rust_expression_notation_circuit(q))
///
/// This will give the following code (`use` and final `;` added for doctest):
/// ```
/// use rust_circuit::{circuit::*, sv};
/// {
///     let node0 = ScalarConstant::new(0.2, sv![3], Some("a".to_owned())).rc();
///     let node1 = ScalarConstant::new(0.5, sv![3], Some("ScalarConstant".to_owned())).rc();
///     let node2 = Add::nrc(vec![node0.clone(), node1.clone()], Some("s".to_owned()));
///     Concat::nrc(
///         vec![node0.clone(), node2.clone()],
///         0,
///         Some("cat".to_owned()),
///     )
/// };
/// ```
#[pyfunction(tensors_as_randn = "false")]
pub fn rust_expression_notation_circuit(circuit: CircuitRc, tensors_as_randn: bool) -> String {
    // Possible improvements:
    // * better variable names (if the node has a name that is a valid Rust identifier, doesn't shadow anything, ..., use that)
    // * inline single use variables?

    // context/environment of circuit variable names so far
    let mut context: HashMap<CircuitRc, String> = HashMap::new();

    // make a source code block defining each node in a topologically sorted order
    let order = toposort_circuit(circuit);
    let mut source = String::with_capacity(order.len() * 60);
    source.push_str("{\n");

    for (i, node) in order.iter().enumerate() {
        // we will use the very creative naming scheme of node0, node1, ...
        // later we should leverage the names most nodes already have
        // (needs to be unique, a valid Rust identifier, and can't shadow important stuff)
        let key: CircuitRc = CircuitRc(node.0.clone());
        context.insert(key.clone(), format!("node{}", i));

        let node_source = repr_circuit_one_level(node, &context, tensors_as_randn);
        if i < order.len() - 1 {
            source.push_str(format!("    let {} = {};\n", context[node], node_source).as_str());
        } else {
            // the block needs to return the top level circuit, which is the last element of the top sort
            source.push_str(format!("    {}\n", node_source).as_str());
        }
    }
    source.push('}');
    source
    // timed!(rustfmt_string(&source))
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
