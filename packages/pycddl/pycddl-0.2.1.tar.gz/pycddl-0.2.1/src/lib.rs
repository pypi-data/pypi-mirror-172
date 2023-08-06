use cddl::ast::CDDL;
use ouroboros::self_referencing;
use pyo3::{
    create_exception,
    exceptions::{PyException, PyValueError},
    prelude::*,
};

#[pyclass]
struct Schema {
    // We need to do a song-and-dance with an inner struct because #[pyclass]
    // doesn't like generic classes, and #[pyclass] and #[self_referencing]
    // conflict.
    inner: SchemaImpl,
}

#[self_referencing]
struct SchemaImpl {
    // Keep around the underlying data.
    schema_string: String,
    // The parsed schema:
    #[borrows(schema_string)]
    #[covariant]
    schema: CDDL<'this>,
}

#[pymethods]
impl Schema {
    #[new]
    fn new(schema_string: String) -> PyResult<Self> {
        let inner = SchemaImplTryBuilder {
            schema_string,
            schema_builder: |s: &String| CDDL::from_slice(s.as_bytes()),
        }
        .try_build()
        .map_err(PyValueError::new_err)?;
        Ok(Schema { inner })
    }

    fn __repr__(&self) -> String {
        format!(r#"Schema("""{}""")"#, self.inner.borrow_schema_string())
    }

    fn validate_cbor(&self, cbor: &[u8]) -> PyResult<()> {
        self.inner
            .borrow_schema()
            .validate(cbor, None)
            .map_err(|e| ValidationError::new_err(format!("{}", e)))?;
        Ok(())
    }
}

create_exception!(pycddl, ValidationError, PyException);

#[pymodule]
fn pycddl(py: Python, m: &PyModule) -> PyResult<()> {
    m.add("ValidationError", py.get_type::<ValidationError>())?;
    m.add_class::<Schema>()?;
    Ok(())
}
