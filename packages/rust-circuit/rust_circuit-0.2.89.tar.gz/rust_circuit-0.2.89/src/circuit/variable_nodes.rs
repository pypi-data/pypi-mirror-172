use std::collections::BTreeMap;

use super::{
    CachedCircuitInfo, CircuitConstructionError, CircuitNode, CircuitNodeAutoName, CircuitRc,
    ScalarConstant, TensorEvalError,
};
use crate::new_rc_unwrap;
use crate::py_types::PyUuid;
use crate::{
    circuit::PyCircuitBase,
    circuit_node_auto_impl, circuit_node_extra_impl, new_rc,
    py_types::Tensor,
    pyo3_prelude::*,
    tensor_util::{Shape, TorchDeviceDtype},
};
use macro_rules_attribute::apply;
use uuid::uuid;
use uuid::Uuid;

/// Tags a Circuit with a UUID. Use this to make two otherwise equal nodes distinct.
/// This is used to make two independent samplings of the random variable, whereas without making them distinct,
/// they would be references to the same samplings
///
/// - *Why is this useful?* The `probs_and_group` attribute of random variables
///   groups RVs that have the "same randomness" somehow. Usually used as the
///   `.probs_and_group` attribute of `DiscreteVar`, to prevent several uniform
///   `DiscreteVar`s with the same number of samples, from being sampled all
///   together.
#[pyclass(extends=PyCircuitBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct AutoTag {
    #[pyo3(get)]
    pub node: CircuitRc,
    pub uuid: Uuid,
    name: Option<String>,
    info: CachedCircuitInfo,
}

impl AutoTag {
    #[apply(new_rc)]
    pub fn new(node: CircuitRc, uuid: Uuid, name: Option<String>) -> (Self) {
        let mut out = Self {
            node,
            uuid,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        out.init_info().unwrap()
    }
}

impl CircuitNodeAutoName for AutoTag {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| self.node.name().map(|n| format!("AutoTag {}", n)))
    }
}

circuit_node_extra_impl!(AutoTag);

impl CircuitNode for AutoTag {
    circuit_node_auto_impl!("63fdc4ce-2f1b-40b3-b8b6-13991b54cbd7");

    fn compute_shape(&self) -> Shape {
        self.node.compute_shape()
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&self.node.info().hash);
        hasher.update(self.uuid.as_bytes());
        hasher
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        vec![(0..self.node.info().rank()).map(Some).collect()]
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        Box::new(std::iter::once(self.node.clone()))
    }

    fn map_children_enumerate<F, E>(&self, mut f: F) -> Result<Self, CircuitConstructionError>
    where
        Self: Sized,
        CircuitConstructionError: From<E>,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc, E>,
    {
        Ok(Self::new(
            f(0, self.node.clone())?,
            self.uuid,
            self.name.clone(),
        ))
    }

    fn eval_tensors(
        &self,
        tensors: &[Tensor],
        device_dtype: &TorchDeviceDtype,
    ) -> Result<Tensor, TensorEvalError> {
        self.node.eval_tensors(tensors, device_dtype)
    }
}

#[pymethods]
impl AutoTag {
    #[cfg(feature = "real-pyo3")]
    #[new]
    fn py_new(
        node: CircuitRc,
        uuid: PyUuid,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<AutoTag>> {
        let out = Self::new(node, uuid.0, name);
        Ok(out.into_init())
    }

    #[getter]
    fn uuid(&self) -> PyUuid {
        PyUuid(self.uuid)
    }

    /// Creates a new AutoTag with a random UUID.
    #[staticmethod]
    pub fn new_with_random_uuid(node: CircuitRc, name: Option<String>) -> Self {
        Self::new(node, Uuid::new_v4(), name)
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct DiscreteVar {
    #[pyo3(get)]
    pub values: CircuitRc,
    #[pyo3(get)]
    pub probs_and_group: CircuitRc,
    name: Option<String>,
    info: CachedCircuitInfo,
}

impl DiscreteVar {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        values: CircuitRc,
        probs_and_group: CircuitRc,
        name: Option<String>,
    ) -> (Result<Self, CircuitConstructionError>) {
        if probs_and_group.info().rank() != 1 {
            return Err(CircuitConstructionError::DiscreteVarProbsMustBe1d {
                shape: probs_and_group.info().shape.clone(),
            });
        }
        if values.info().rank() < 1 {
            return Err(CircuitConstructionError::DiscreteVarNoSamplesDim {});
        }
        if values.info().shape[0] != probs_and_group.info().shape[0] {
            return Err(CircuitConstructionError::DiscreteVarWrongSamplesDim {
                node: values.info().shape[0],
                probs: probs_and_group.info().shape[0],
            });
        }
        let mut out = Self {
            values,
            probs_and_group,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        out.init_info()
    }
}

impl CircuitNodeAutoName for DiscreteVar {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            if self.probs_and_group.name().is_none() && self.values.name().is_none() {
                None
            } else {
                Some(format!(
                    "DiscreteVar {} {}",
                    self.values.name().unwrap_or(""),
                    self.probs_and_group.name().unwrap_or("")
                ))
            }
        })
    }
}

circuit_node_extra_impl!(DiscreteVar);

impl CircuitNode for DiscreteVar {
    circuit_node_auto_impl!("1bd791cd-8460-496d-8cf5-303baa3cd226");

    fn compute_shape(&self) -> Shape {
        self.values.info().shape[1..].iter().cloned().collect()
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&self.values.info().hash);
        hasher.update(&self.probs_and_group.info().hash);
        hasher
    }

    fn compute_can_be_sampled(&self) -> bool {
        true
    }

    fn compute_is_constant(&self) -> bool {
        false
    }

    fn compute_is_explicitly_computable(&self) -> bool {
        false
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        vec![
            std::iter::once(None)
                .chain((0..self.info().rank()).map(Some))
                .collect(),
            vec![None],
        ]
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        Box::new([self.values.clone(), self.probs_and_group.clone()].into_iter())
    }

    fn map_children_enumerate<F, E>(&self, mut f: F) -> Result<Self, CircuitConstructionError>
    where
        Self: Sized,
        CircuitConstructionError: From<E>,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc, E>,
    {
        Self::try_new(
            f(0, self.values.clone())?,
            f(1, self.probs_and_group.clone())?,
            self.name.clone(),
        )
    }

    fn eval_tensors(
        &self,
        _tensors: &[Tensor],
        _device_dtype: &TorchDeviceDtype,
    ) -> Result<Tensor, TensorEvalError> {
        Err(TensorEvalError::NotExplicitlyComputable {
            circuit: self.clone().rc(),
        })
    }
}

#[pymethods]
impl DiscreteVar {
    #[cfg(feature = "real-pyo3")]
    #[new]
    fn py_new(
        values: CircuitRc,
        probs_and_group: CircuitRc,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<DiscreteVar>> {
        let out = Self::try_new(values, probs_and_group, name)?;
        Ok(out.into_init())
    }
    #[staticmethod]
    pub fn new_uniform(
        values: CircuitRc,
        name: Option<String>,
    ) -> Result<Self, CircuitConstructionError> {
        if values.info().rank() < 1 {
            return Err(CircuitConstructionError::DiscreteVarNoSamplesDim {});
        }
        Self::try_new(
            values.clone(),
            AutoTag::new_with_random_uuid(
                ScalarConstant::nrc(
                    1.0 / (values.info().shape[0] as f64),
                    values.info().shape[1..].iter().cloned().collect(),
                    None,
                ),
                None,
            )
            .rc(),
            name,
        )
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct StoredCumulantVar {
    #[pyo3(get)]
    pub cumulants: BTreeMap<usize, CircuitRc>, // using btreemap so it always iterates in order
    pub uuid: Uuid,
    name: Option<String>,
    info: CachedCircuitInfo,
}

impl StoredCumulantVar {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        cumulants: BTreeMap<usize, CircuitRc>,
        uuid: Uuid,
        name: Option<String>,
    ) -> (Result<Self, CircuitConstructionError>) {
        if !cumulants.contains_key(&1) || !cumulants.contains_key(&2) {
            return Err(CircuitConstructionError::StoredCumulantVarNeedsMeanVariance {});
        }
        if cumulants.contains_key(&0) {
            return Err(
                CircuitConstructionError::StoredCumulantVarInvalidCumulantNumber { number: 0 },
            );
        }
        let shape = &cumulants[&1].info().shape;
        for (k, v) in cumulants.iter() {
            let shape_here: Shape = shape
                .iter()
                .cycle()
                .take(k * shape.len())
                .copied()
                .collect();
            if shape_here != v.info().shape {
                return Err(
                    CircuitConstructionError::StoredCumulantVarCumulantWrongShape {
                        cumulant_shape: v.info().shape.clone(),
                        cumulant_number: *k,
                        base_shape: shape.clone(),
                    },
                );
            }
        }
        let mut out = Self {
            cumulants,
            uuid,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        out.init_info()
    }

    pub fn new_mv(
        mean: CircuitRc,
        variance: CircuitRc,
        higher_cumulants: BTreeMap<usize, CircuitRc>,
        uuid: Option<Uuid>,
        name: Option<String>,
    ) -> Result<Self, CircuitConstructionError> {
        let mut higher_cumulants = higher_cumulants;
        higher_cumulants.insert(1, mean);
        higher_cumulants.insert(2, variance);
        Self::try_new(
            higher_cumulants,
            uuid.unwrap_or_else(|| Uuid::new_v4()),
            name,
        )
    }
}

impl CircuitNodeAutoName for StoredCumulantVar {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            if self.cumulants.values().all(|x| x.name().is_none()) {
                None
            } else {
                Some(
                    "StoredCumulantVar ".to_owned()
                        + &self
                            .cumulants
                            .values()
                            .filter_map(|x| x.name().map(|y| y.to_owned()))
                            .collect::<Vec<String>>()
                            .join(", "),
                )
            }
        })
    }
}

circuit_node_extra_impl!(StoredCumulantVar);

impl CircuitNode for StoredCumulantVar {
    circuit_node_auto_impl!("f36da959-d160-484d-b6b8-7685ef7521c0");

    fn compute_shape(&self) -> Shape {
        self.cumulants[&1].info().shape.clone()
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        for (k, v) in &self.cumulants {
            hasher.update(&k.to_le_bytes());
            hasher.update(&v.info().hash);
        }
        hasher.update(self.uuid.as_bytes());
        hasher.update(uuid!("02083055-8b54-42e1-90c6-2f5d778e43b5").as_bytes());

        hasher
    }

    fn compute_can_be_sampled(&self) -> bool {
        true
    }

    fn compute_is_constant(&self) -> bool {
        false
    }

    fn compute_is_explicitly_computable(&self) -> bool {
        false
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        self.cumulants
            .values()
            .map(|x| vec![None; x.info().rank()])
            .collect()
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        Box::new(self.cumulants.values().cloned())
    }

    fn map_children_enumerate<F, E>(&self, mut f: F) -> Result<Self, CircuitConstructionError>
    where
        Self: Sized,
        CircuitConstructionError: From<E>,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc, E>,
    {
        Self::try_new(
            self.cumulants
                .iter()
                .enumerate()
                .map(|(i, (k, v))| f(i, v.clone()).map(|z| (*k, z)))
                .collect::<Result<BTreeMap<_, _>, _>>()?,
            self.uuid,
            self.name.clone(),
        )
    }

    fn eval_tensors(
        &self,
        _tensors: &[Tensor],
        _device_dtype: &TorchDeviceDtype,
    ) -> Result<Tensor, TensorEvalError> {
        Err(TensorEvalError::NotExplicitlyComputable {
            circuit: self.clone().rc(),
        })
    }
}

#[pymethods]
impl StoredCumulantVar {
    #[cfg(feature = "real-pyo3")]
    #[new]
    fn py_new(
        cumulants: BTreeMap<usize, CircuitRc>,
        uuid: Option<PyUuid>,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<StoredCumulantVar>> {
        let uuid = uuid.unwrap_or_else(|| PyUuid(Uuid::new_v4()));
        let out = Self::try_new(cumulants, uuid.0, name)?;
        Ok(out.into_init())
    }

    #[getter]
    fn uuid(&self) -> PyUuid {
        PyUuid(self.uuid)
    }

    #[staticmethod]
    #[pyo3(name = "new_mv")]
    pub fn new_mv_py(
        mean: CircuitRc,
        variance: CircuitRc,
        higher_cumulants: BTreeMap<usize, CircuitRc>,
        uuid: Option<PyUuid>,
        name: Option<String>,
    ) -> Result<Self, CircuitConstructionError> {
        Self::new_mv(mean, variance, higher_cumulants, uuid.map(|x| x.0), name)
    }
}
