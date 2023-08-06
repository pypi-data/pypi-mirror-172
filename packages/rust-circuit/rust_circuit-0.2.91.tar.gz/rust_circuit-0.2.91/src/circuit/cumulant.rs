use std::cmp::Ordering;

use super::{
    Add, CachedCircuitInfo, CircResult, CircuitConstructionError, CircuitNode, CircuitNodeAutoName,
    CircuitRc, Rearrange, ScalarConstant, TensorEvalError,
};
use crate::all_imports::Shape;
use crate::all_imports::{OpSize, RearrangeSpec};
use crate::circuit::Einsum;
use crate::circuit::PyCircuitBase;
use crate::py_types::scalar_to_tensor;
use crate::tensor_util::TorchDeviceDtype;
use crate::util::cumsum;
use crate::{circuit_node_auto_impl, circuit_node_extra_impl, new_rc, pyo3_prelude::*, sv};
use macro_rules_attribute::apply;
use std::iter::once;

#[pyclass(extends=PyCircuitBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct Cumulant {
    #[pyo3(get)]
    pub nodes: Vec<CircuitRc>,
    info: CachedCircuitInfo,
    name: Option<String>,
}

pub fn circuit_order_cmp_name_first(a: &CircuitRc, b: &CircuitRc) -> Ordering {
    a.name().cmp(&b.name()).then(a.cmp(&b))
}

impl Cumulant {
    #[apply(new_rc)]
    pub fn new(nodes: Vec<CircuitRc>, name: Option<String>) -> (Self) {
        let mut out = Self {
            nodes,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        out.init_info().unwrap()
    }
}

circuit_node_extra_impl!(Cumulant);

impl CircuitNode for Cumulant {
    circuit_node_auto_impl!("0954a2b9-e138-480d-b967-305cfc6c5a2b");

    fn compute_shape(&self) -> Shape {
        self.nodes
            .iter()
            .flat_map(|child| &child.info().shape)
            .cloned()
            .collect()
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        for node in &self.nodes {
            hasher.update(&node.info().hash);
        }
        hasher
    }

    // default impl of compute can_be_sampled + is_explicitly_computable

    fn compute_is_constant(&self) -> bool {
        true
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        Box::new(self.nodes.iter().cloned())
    }

    fn map_children_enumerate<F, E>(&self, mut f: F) -> Result<Self, CircuitConstructionError>
    where
        CircuitConstructionError: From<E>,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc, E>,
    {
        Ok(Self::new(
            self.nodes
                .iter()
                .enumerate()
                .map(move |(i, circ)| f(i, circ.clone()))
                .collect::<Result<Vec<_>, _>>()?,
            self.name.clone(),
        ))
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let mut place = 0;
        self.nodes
            .iter()
            .map(|child| {
                let rank = child.info().rank();
                place += rank;
                (place - rank..place).map(|i| Some(i)).collect()
            })
            .collect()
    }

    fn eval_tensors(
        &self,
        tensors: &[crate::py_types::Tensor],
        device_dtype: &TorchDeviceDtype,
    ) -> Result<crate::py_types::Tensor, super::TensorEvalError> {
        if !self.info().is_explicitly_computable {
            return Err(TensorEvalError::NotExplicitlyComputable {
                circuit: self.clone().rc(),
            });
        }

        match (&self.nodes[..], tensors) {
            ([], []) => return Ok(scalar_to_tensor(1., sv![], device_dtype.clone())?),
            ([_], [t]) => return Ok(t.clone()),
            _ => unreachable!(),
        }
    }
}

impl CircuitNodeAutoName for Cumulant {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            if self.children().any(|x| x.name().is_none()) {
                None
            } else {
                Some(
                    "K I ".to_owned()
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
                            .join(" I "),
                )
            }
        })
    }
}

#[pymethods]
impl Cumulant {
    #[cfg(feature = "real-pyo3")]
    #[new]
    fn new_py(
        nodes: Vec<CircuitRc>,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<Cumulant>> {
        let out = Cumulant::new(nodes, name);

        Ok(out.into_init())
    }

    /// Make a cumulant where the nodes are in canonical order, then rearrange to the specified order
    #[staticmethod]
    pub fn new_canon_rearrange(
        nodes: Vec<CircuitRc>,
        name: Option<String>,
    ) -> Result<Rearrange, CircuitConstructionError> {
        let mut sorting_perm: Vec<usize> = (0..nodes.len()).collect();
        sorting_perm.sort_by(|a, b| circuit_order_cmp_name_first(&nodes[*a], &nodes[*b]));

        let nodes_sorted = sorting_perm.iter().map(|i| nodes[*i].clone()).collect();
        let cum = Cumulant::new(nodes_sorted, name.clone().map(|i| "canon ".to_owned() + &i));
        let sections = nodes
            .iter()
            .map(|child| child.info().rank())
            .collect::<Vec<_>>();
        let perm_blocks = permutation_from_block_permutation(sorting_perm, sections);
        Rearrange::try_new(
            cum.clone().rc(),
            RearrangeSpec::new(
                perm_blocks.into_iter().map(|i| sv![i as u8]).collect(),
                (0..cum.info().rank()).map(|i| sv![i as u8]).collect(),
                sv![OpSize::NONE;cum.info().rank()],
            ),
            name,
        )
    }

    #[getter]
    pub fn cumulant_number(&self) -> usize {
        self.nodes.len()
    }

    pub fn equivalent_explicitly_computable_circuit(&self) -> CircResult {
        if self.info().is_explicitly_computable {
            return match self.nodes.len() {
                0 => Ok(ScalarConstant::nrc(0.0, sv![], None)),
                1 => Ok(self.nodes[0].clone()),
                _ => Ok(ScalarConstant::nrc(0.0, self.info().shape.clone(), None)),
            };
        }
        Err(CircuitConstructionError::NoEquivalentExplicitlyComputable {})
    }

    /// formula from https://en.wikipedia.org/wiki/Cumulant#Joint_cumulants
    pub fn basic_expectation(&self) -> CircuitRc {
        let partition_circuits = partitions(self.nodes.len())
            .map(|partition| {
                let multiplier =
                    ScalarConstant::nrc(CUMULANT_MULTIPLIERS[partition.len()], sv![], None);
                let expectations = partition.iter().map(|x| {
                    product_expectation(x.iter().map(|i| self.nodes[*i].clone()).collect()).rc()
                });
                let node_permutation: Vec<usize> = partition.iter().cloned().flatten().collect();
                let idx_permutation = permutation_from_block_permutation(
                    node_permutation.clone(),
                    node_permutation
                        .iter()
                        .map(|i| self.nodes[*i].info().rank())
                        .collect(),
                );
                Einsum::new_outer_product(
                    expectations.chain(once(multiplier)).collect(),
                    None,
                    Some(idx_permutation),
                )
                .rc()
            })
            .collect();
        Add::nrc(partition_circuits, None)
    }

    // /// source: https://arxiv.org/pdf/1701.05420.pdf
    // pub fn factored_cumulant_expectation_and_aux(&self)->(CircuitRc,Cumulant,Vec<CircuitRc>){
    //     if self.nodes.len()<=1{
    //         return (self.clone(),self.clone(),vec![])
    //     }
    //     centered_mom = Cumulant::new()
    // }
    // pub fn factored_cumulant_expectation(&self)->CircuitRc{
    //     self.factored_cumulant_expectation_and_aux().0
    // }

    // def factored_cumulant_expectation_rewrite_full(
    //     cumulant: Cumulant, apply_to_nested: Callable[[Cumulant], Circuit] = lambda x: x
    // ) -> Tuple[Circuit, Cumulant, List[Circuit]]:
    //     """source: https://arxiv.org/pdf/1701.05420.pdf"""
    //     if len(cumulant.circuits) <= 1:
    //         return cumulant, cumulant, []

    //     centered_mom = Cumulant(
    //         (centered_product(*cumulant.circuits, apply_to_centering=apply_to_nested),),
    //         name=f"{cumulant.name}_centered_moment",
    //     )
    //     sub: List[Circuit] = []

    //     for p in partition(list(enumerate(cumulant.circuits))):
    //         if any(len(b) < 2 for b in p) or len(p) == 1:
    //             continue

    //         cumulants = [Cumulant.from_spec(CircuitMultiset.from_values(x[1] for x in b)).rename_to_canonical() for b in p]

    //         permutation = dim_permutation_for_circuits(p, [m.circuits for m in cumulants], len(cumulant.circuits))

    //         new_out = Einsum.outer_product(*cumulants, out_axes_permute=permutation)
    //         assert new_out.shape == tuple(itertools.chain.from_iterable(c.shape for c in cumulant.circuits))
    //         sub.append(new_out)

    //     return (
    //         Add.from_weighted_list([(centered_mom, 1.0), *[(v, -1.0) for v in sub]], name=f"{cumulant.name}_decompose"),
    //         centered_mom,
    //         sub,
    //     )

    // def factored_cumulant_expectation_rewrite(
    //     cumulant: Cumulant, apply_to_nested: Callable[[Cumulant], Circuit] = lambda x: x
    // ) -> Circuit:
    //     return factored_cumulant_expectation_rewrite_full(cumulant, apply_to_nested=apply_to_nested)[0]
}

pub fn product_expectation(nodes: Vec<CircuitRc>) -> Cumulant {
    let product = Einsum::new_outer_product(nodes, None, None).rc();
    Cumulant::new(vec![product], None)
}
/// this uses lots of boxed iterators. this may be faster, but is annoying and confusing.
pub fn partitions(n: usize) -> Box<dyn Iterator<Item = Vec<Vec<usize>>>> {
    match n {
        0 => Box::new(once(vec![])),
        1 => Box::new(once(vec![vec![0]])),
        _ => {
            let first = n - 1;
            let smallers = partitions(n - 1);
            Box::new(smallers.flat_map(move |smaller| {
                let smaller_copy = smaller.clone(); // for borrow checker reasons
                Box::new(
                    smaller
                        .clone()
                        .into_iter()
                        .enumerate()
                        .map(move |(i, subset)| {
                            smaller_copy
                                .clone()
                                .into_iter()
                                .take(i)
                                .chain(once(
                                    subset.iter().cloned().chain(once(first.clone())).collect(),
                                ))
                                .chain(smaller_copy.clone().into_iter().skip(i + 1))
                                .collect()
                        })
                        .chain(once(
                            smaller
                                .clone()
                                .into_iter()
                                .chain([vec![first.clone()]])
                                .collect(),
                        )),
                )
            }))
        }
    }
}

pub fn permutation_from_block_permutation(
    permutation: Vec<usize>,
    block_sizes: Vec<usize>,
) -> Vec<usize> {
    let starts = cumsum(&block_sizes);
    permutation
        .iter()
        .flat_map(|i| (starts[*i]..starts[*i] + block_sizes[*i]))
        .collect()
}

#[test]
fn test_permutation_to_block() {
    dbg!(permutation_from_block_permutation(
        vec![1, 0, 2],
        vec![1, 2, 3]
    ));
}

#[test]
fn test_partition() {
    let r: Vec<_> = partitions(3).collect();
    dbg!(&r);
}

/// CUMULANT_MULTIPLIERS[i] = i!*(-1)^i
#[rustfmt::skip]
static CUMULANT_MULTIPLIERS:[f64;64] = [1.0, -1.0, 2.0, -6.0, 24.0, -120.0, 720.0, -5040.0, 40320.0, -362880.0, 3628800.0, -39916800.0, 479001600.0, -6227020800.0, 87178291200.0, -1307674368000.0, 20922789888000.0, -355687428096000.0, 6402373705728000.0, -1.21645100408832e+17, 2.43290200817664e+18, -5.109094217170944e+19, 1.1240007277776077e+21, -2.585201673888498e+22, 6.204484017332394e+23, -1.5511210043330986e+25, 4.0329146112660565e+26, -1.0888869450418352e+28, 3.0488834461171387e+29, -8.841761993739702e+30, 2.6525285981219107e+32, -8.222838654177922e+33, 2.631308369336935e+35, -8.683317618811886e+36, 2.9523279903960416e+38, -1.0333147966386145e+40, 3.7199332678990125e+41, -1.3763753091226346e+43, 5.230226174666011e+44, -2.0397882081197444e+46, 8.159152832478977e+47, -3.345252661316381e+49, 1.40500611775288e+51, -6.041526306337383e+52, 2.658271574788449e+54, -1.1962222086548019e+56, 5.502622159812089e+57, -2.5862324151116818e+59, 1.2413915592536073e+61, -6.082818640342675e+62, 3.0414093201713376e+64, -1.5511187532873822e+66, 8.065817517094388e+67, -4.2748832840600255e+69, 2.308436973392414e+71, -1.2696403353658276e+73, 7.109985878048635e+74, -4.0526919504877214e+76, 2.3505613312828785e+78, -1.3868311854568984e+80, 8.32098711274139e+81, -5.075802138772248e+83, 3.146997326038794e+85, -1.98260831540444e+87];
