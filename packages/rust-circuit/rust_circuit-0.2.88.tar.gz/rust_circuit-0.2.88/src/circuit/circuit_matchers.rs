use std::sync::Arc;

use pyo3::exceptions::PyValueError;
use regex::{Captures, Regex};

use super::{visit_circuit_fallable, CircuitNode, CircuitNodeUnion, CircuitRc};
use crate::hashmaps::AHashSet as HashSet;
use crate::pyo3_prelude::*;

type RawMatcher = Arc<dyn Fn(CircuitRc) -> Result<bool, PyErr>>;

#[derive(Clone)]
#[pyclass(unsendable)]
pub struct Matcher(RawMatcher);
#[pymethods]
impl Matcher {
    fn __call__(&self, _py: Python<'_>, circuit: CircuitRc) -> Result<bool, PyErr> {
        self.0(circuit)
    }

    pub fn call(&self, circuit: CircuitRc) -> Result<bool, PyErr> {
        self.0(circuit)
    }

    pub fn get(&self, circuit: CircuitRc) -> Result<HashSet<CircuitRc>, PyErr> {
        let mut result = HashSet::new();
        visit_circuit_fallable(circuit, |x| {
            if self.call(x.clone())? {
                result.insert(x);
            }
            return Ok::<(), PyErr>(());
        })?;
        Ok(result)
    }

    pub fn get_first(&self, circuit: CircuitRc) -> Result<Option<CircuitRc>, PyErr> {
        let mut result: Option<CircuitRc> = None;
        let mut err = visit_circuit_fallable(circuit, |x| {
            if self.call(x.clone())? {
                result = Some(x);
                return Err(PyValueError::new_err("just stopping, everything is fine"));
            }
            return Ok::<(), PyErr>(());
        });
        if err.is_err()
            && err
                .as_ref()
                .err()
                .unwrap()
                .to_string()
                .contains("just stopping, everything is fine")
        {
            err = Ok(())
        }
        err?;
        Ok(result)
    }

    #[staticmethod]
    pub fn new_py(pyfunc: PyObject) -> Matcher {
        Matcher(Arc::new(move |n| {
            Python::with_gil(|py| pyfunc.call1(py, (n,)).and_then(|r| r.extract(py)))
        }))
    }

    #[staticmethod]
    pub fn new_regex(string: String) -> Result<Matcher, PyErr> {
        let regex = Regex::new(&string).map_err(|e| PyValueError::new_err(format!("{:?}", e)))?;
        Ok(Matcher(Arc::new(move |n| {
            Ok(n.name().map(|s| regex.is_match(s)).unwrap_or(false))
        })))
    }

    #[staticmethod]
    pub fn new_regex_invert_dot(string: String) -> Result<Matcher, PyErr> {
        let string =
            Regex::new(r"(\.)|(.)")
                .unwrap()
                .replace_all(&string, |captures: &Captures| {
                    if captures.get(1).is_some() {
                        ".".to_owned()
                    } else {
                        r"\.".to_owned()
                    }
                });
        let regex = Regex::new(&string).map_err(|e| PyValueError::new_err(format!("{:?}", e)))?;
        Ok(Matcher(Arc::new(move |n| {
            Ok(n.name().map(|s| regex.is_match(s)).unwrap_or(false))
        })))
    }

    #[staticmethod]
    pub fn new_variant(variant_strings: HashSet<String>) -> Matcher {
        Matcher(Arc::new(move |n| {
            Ok(variant_strings.contains(&n.variant_string()))
        }))
    }

    #[staticmethod]
    pub fn new_not(matcher: Matcher) -> Matcher {
        Matcher(Arc::new(move |n| matcher.call(n).map(|b| !b)))
    }
    #[staticmethod]
    pub fn new_and(matchers: Vec<Matcher>) -> Matcher {
        Matcher(Arc::new(move |n| {
            matchers
                .iter()
                .map(|m| m.call(n.clone()))
                .collect::<Result<Vec<_>, _>>()
                .map(|v| v.iter().all(|z| *z))
        }))
    }
    #[staticmethod]
    pub fn new_or(matchers: Vec<Matcher>) -> Matcher {
        Matcher(Arc::new(move |n| {
            matchers
                .iter()
                .map(|m| m.call(n.clone()))
                .collect::<Result<Vec<_>, _>>()
                .map(|v| v.iter().all(|z| *z))
        }))
    }
}
