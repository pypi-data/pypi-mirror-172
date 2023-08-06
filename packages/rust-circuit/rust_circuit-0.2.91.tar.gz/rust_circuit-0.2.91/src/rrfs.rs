use std::os::unix::prelude::OsStrExt;

use crate::pyo3_prelude::*;
use crate::{
    circuit::ArrayConstant,
    py_types::{Tensor, PY_UTILS},
};
use base16::encode_lower;

pub fn get_rrfs_dir() -> String {
    std::env::var("RRFS_DIR").unwrap_or_else(|_e| std::env::var("HOME").unwrap() + "/rrfs")
}

pub fn get_tensor_by_hash_dir() -> String {
    std::env::var("TENSORS_BY_HASH_DIR")
        .unwrap_or_else(|_| get_rrfs_dir() + "/circuit_tensors_by_hash")
}

#[pyfunction]
pub fn tensor_from_hash(hash_base16: &str) -> Result<Tensor, PyErr> {
    let hashdir = get_tensor_by_hash_dir() + "/" + hash_base16 + ".pt";
    Python::with_gil(|py| {
        PY_UTILS
            .torch
            .getattr(py, "load")
            .unwrap()
            .call(py, (hashdir,), None)
            .map(|z| z.extract(py).unwrap())
    })
}

#[pyfunction]
pub fn tensor_from_hash_prefix(hash_base16: &str) -> Result<Tensor, PyErr> {
    let hash_base16_bytes = hash_base16.as_bytes();
    let dir: Vec<_> = std::fs::read_dir(get_tensor_by_hash_dir())
        .unwrap()
        .into_iter()
        .filter(|x| {
            let nm = x.as_ref().unwrap().file_name();
            let name_bytes = nm.as_bytes();
            name_bytes.len() >= hash_base16_bytes.len()
                && &name_bytes[0..hash_base16_bytes.len()] == hash_base16_bytes
        })
        .collect();
    if dir.len() > 1 {
        return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "prefix ambiguous",
        ));
    }
    if dir.is_empty() {
        return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "prefix not found",
        ));
    }
    tensor_from_hash(
        dir[0]
            .as_ref()
            .unwrap()
            .file_name()
            .to_str()
            .unwrap()
            .strip_suffix(".pt")
            .unwrap(),
    )
}

pub fn arrayconstant_from_hash(
    name: Option<String>,
    hash_base16: &str,
) -> Result<ArrayConstant, PyErr> {
    tensor_from_hash(hash_base16).map(|value| ArrayConstant::new(value, name))
}

pub fn arrayconstant_from_hash_prefix(
    name: Option<String>,
    hash_base16: &str,
) -> Result<ArrayConstant, PyErr> {
    tensor_from_hash_prefix(hash_base16).map(|value| ArrayConstant::new(value, name))
}

#[pyfunction]
pub fn save_tensor_rrfs(tensor: Tensor) -> Result<String, PyErr> {
    let tensor = tensor.hashed();
    let hash_base16 = encode_lower(tensor.hash().unwrap());
    let hashdir = get_tensor_by_hash_dir() + "/" + &hash_base16 + ".pt";
    Python::with_gil(|py| {
        PY_UTILS
            .torch
            .getattr(py, "save")
            .unwrap()
            .call(py, (tensor.tensor(), hashdir), None)
            .map(|_| hash_base16)
    })
}
