use pyo3::prelude::*;
use std::f64;



/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyclass]
struct Foo {
    a : i128,
    b :f64,
}



/// A Python module implemented in Rust.
#[pymodule]
fn zyhsub(_py: Python, m: &PyModule) -> PyResult<()> {
    let foo = Foo{a:3232352352352,b:3.14159265359398979};
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_class::<Foo>()?;
    m.add("foo",foo);
    m.add("PI",3.1415926_f64);
    m.add("inf",f64::INFINITY);
    m.add("nan",f64::NAN);
    m.add("MIN_10_EXP",f64::MIN_10_EXP);
    Ok(()) }





