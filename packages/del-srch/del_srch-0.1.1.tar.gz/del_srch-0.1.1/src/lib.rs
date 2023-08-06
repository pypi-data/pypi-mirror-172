// use numpy::ndarray::{Array2, ArrayD, ArrayViewD, ArrayViewMutD};
// use numpy::{IntoPyArray, PyArrayDyn, PyReadonlyArrayDyn, PyArray2, PyArray1};
use numpy::{PyReadonlyArray1, PyReadonlyArray2,
            PyArray1};
use pyo3::{pymodule, types::PyModule, PyResult, Python};
use del_misc;

/// A Python module implemented in Rust.
#[pymodule]
fn del_srch(_py: Python, m: &PyModule) -> PyResult<()> {

    #[pyfn(m)]
    fn first_intersection_ray_meshtri3<'a>(
        py: Python<'a>,
        src: PyReadonlyArray1<'a, f32>,
        dir: PyReadonlyArray1<'a, f32>,
        vtx_xyz: PyReadonlyArray2<'a, f32>,
        tri_vtx: PyReadonlyArray2<'a, usize>) -> (&'a PyArray1<f32>, i64)
    {
        use crate::del_misc::srch_bruteforce;
        let res = srch_bruteforce::intersection_meshtri3(
            src.as_slice().unwrap(),
            dir.as_slice().unwrap(),
            vtx_xyz.as_slice().unwrap(),
            tri_vtx.as_slice().unwrap());
        match res {
            None => {
                let a = PyArray1::<f32>::zeros(py,3,true);
                return (a, -1);
            },
            Some(postri) => {
                let a = PyArray1::<f32>::from_slice(py, &postri.0);
                return (a, postri.1 as i64);
            }
        }
    }

    Ok(())
}