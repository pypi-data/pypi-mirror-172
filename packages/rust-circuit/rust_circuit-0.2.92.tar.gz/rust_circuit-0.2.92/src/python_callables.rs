use crate::circuit::{CircuitConstructionError, CircuitRc};
use crate::pyo3_prelude::*;
use macro_rules_attribute::apply;

// py newtype for ()
pub struct PyUnitType;
impl IntoPy<PyObject> for PyUnitType {
    fn into_py(self, py: Python<'_>) -> PyObject {
        py.None()
    }
}
impl<'source> FromPyObject<'source> for PyUnitType {
    fn extract(none: &'source PyAny) -> PyResult<Self> {
        if none.is_none() {
            Ok(PyUnitType)
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                "Expected None, found not none",
            ))
        }
    }
}

#[macro_export]
macro_rules! pycallable{
    {@handle_ty; (); $ex:expr} => {
        {
            ($ex).map(|_ : $crate::python_callables::PyUnitType| ())
        }
    };
    {@handle_ty; $ty:ty; $ex:expr} => { $ex };
    {
        $(#[doc = $doc:literal])*
        #[pyo3(name=$name_string:literal)]
        pub fn $name:ident<F>($arg_name:ident : $arg_ty:ty , $f:ident :F   $(,)?)-> Result<$ret_ty:ty,$err:ty>
        where
        F:$ftype:ident($( ($fn_arg_name:ident , $fn_arg_ty:ty)),*$(,)?)->Result<$fn_ret_ty:ty,_>$(,)?
        { $($tt:tt)* }
    }=>{
        $(#[doc = $doc])*
        pub fn $name<F> ($arg_name : $arg_ty , $f:F)-> Result<$ret_ty,$err>
        where
        F:$ftype($($fn_arg_ty),*)->Result<$fn_ret_ty,$err>
        { $($tt)* }
        paste::paste!{
            pub fn [<$name _unwrap>]<F> ($arg_name : $arg_ty , $f:F)-> $ret_ty
            where
            F:$ftype($($fn_arg_ty),*)->$fn_ret_ty
            {
                $name($arg_name,|$($fn_arg_name),*|Ok($f($($fn_arg_name),*))).unwrap()
            }

            #[pyfunction]
            #[pyo3(name=$name_string)]
            pub fn [<$name _py>]($arg_name : $arg_ty , o:PyObject)-> Result<$ret_ty,$err>{
                $name($arg_name , |$( $fn_arg_name :$fn_arg_ty),*| $crate::pycallable!(@handle_ty; $ret_ty; $crate::pycall!(o,($( $fn_arg_name),*,),$err)))
            }
        }
    };
    // copy but with mut :(
    {
        $(#[doc = $doc:literal])*
        #[pyo3(name=$name_string:literal)]
        pub fn $name:ident<F>($arg_name:ident : $arg_ty:ty , mut $f:ident :F   $(,)?)-> Result<$ret_ty:ty,$err:ty>
        where
        F:$ftype:ident($( ($fn_arg_name:ident , $fn_arg_ty:ty)),*$(,)?)->Result<$fn_ret_ty:ty,_>$(,)?
        { $($tt:tt)* }
    }=>{
        $(#[doc = $doc])*
        #[allow(unused_mut)]
        pub fn $name<F> ($arg_name : $arg_ty , mut $f:F)-> Result<$ret_ty,$err>
        where
        F:$ftype($($fn_arg_ty),*)->Result<$fn_ret_ty,$err>
        { $($tt)* }

        paste::paste!{
            pub fn [<$name _unwrap>]<F> ($arg_name : $arg_ty , mut $f:F)-> $ret_ty
            where
            F:$ftype($($fn_arg_ty),*)->$fn_ret_ty
            {
                $name($arg_name,|$($fn_arg_name),*|Ok($f($($fn_arg_name),*))).unwrap()
            }

            #[pyfunction]
            #[pyo3(name=$name_string)]
            pub fn [<$name _py>]($arg_name : $arg_ty , o:PyObject)-> Result<$ret_ty,$err>{
                $name($arg_name , |$( $fn_arg_name :$fn_arg_ty),*|$crate::pycallable!(@handle_ty; $ret_ty; $crate::pycall!(o,($( $fn_arg_name),*,),$err)))
            }
        }
    };
}

pycallable! {
    #[pyo3(name="deep_map_1")]
    pub fn deep_map_1<F>(circuit: CircuitRc ,f: F) -> Result<CircuitRc, CircuitConstructionError>
    where
        F: Fn((circuit , CircuitRc),) -> Result<CircuitRc, _>
    {
        f(circuit)
    }
}

#[apply(pycallable)]
#[pyo3(name = "deep_map_1")]
pub fn deep_map_2<F>(circuit: CircuitRc, f: F) -> Result<CircuitRc, CircuitConstructionError>
where
    F: Fn((circuit, CircuitRc)) -> Result<CircuitRc, _>,
{
    f(circuit)
}
