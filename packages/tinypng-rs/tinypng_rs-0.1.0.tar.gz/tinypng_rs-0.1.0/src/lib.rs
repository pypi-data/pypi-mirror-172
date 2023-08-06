use pyo3::exceptions::PyIOError;
use pyo3::prelude::*;
use reqwest::{header::LOCATION, Body, Client, Error as ReqwestError, StatusCode};
use tokio::fs::{self, File};
use tokio::io::Error as IoError;

#[derive(Debug)]
pub enum TinyPngError {
    Reqwest(ReqwestError),
    Io(IoError),
    Location(&'static str),
    Status(String),
}



impl From<ReqwestError> for TinyPngError {
    fn from(err: ReqwestError) -> Self {
        TinyPngError::Reqwest(err)
    }
}

impl From<IoError> for TinyPngError {
    fn from(err: IoError) -> Self {
        TinyPngError::Io(err)
    }
}

impl From<(StatusCode, String)> for TinyPngError {
    fn from(res: (StatusCode, String)) -> Self {
        TinyPngError::Status(format!("{} {}", res.0, res.1))
    }
}

impl From<TinyPngError> for PyErr {
    fn from(err: TinyPngError) -> Self {
       match err{
           TinyPngError::Reqwest(e) => PyIOError::new_err(e.to_string()),
           TinyPngError::Io(e) =>  PyIOError::new_err(e.to_string()),
           TinyPngError::Location(e) =>PyIOError::new_err(e.to_string()),
           TinyPngError::Status(e) => PyIOError::new_err(e.to_string()),
       }
    }
}

pub const REGISTER_URL: &str = "https://tinypng.com/developers";
pub const API_URL: &str = "https://api.tinify.com/shrink";

pub async fn compress_file(key:String,from: String, to: String) -> Result<(u64, u64), TinyPngError> {
    let file = File::open(&from).await.map_err(TinyPngError::from)?;
    let input_size = file.metadata().await.map_err(TinyPngError::from)?.len();

    let res = Client::new()
        .post(API_URL)
        .basic_auth("api", Some(key))
        .body(Body::from(file))
        .send()
        .await
        .map_err(TinyPngError::from)?;

    if res.status() != 201 {
        return Err(TinyPngError::from((
            res.status(),
            res.text().await.unwrap_or_default(),
        )));
    }

    let url = res
        .headers()
        .get(LOCATION)
        .ok_or(TinyPngError::Location("Location header not found"))?
        .to_str()
        .map_err(|_| TinyPngError::Location("Location header not valid UTF-8"))?;

    let output_size = download_file(url, &to).await?;

    Ok((input_size, output_size))
}

async fn download_file(url: &str, path: &str) -> Result<u64, TinyPngError> {
    let res = Client::new()
        .get(url)
        .send()
        .await
        .map_err(TinyPngError::from)?;

    if res.status() != 200 {
        return Err(TinyPngError::from((
            res.status(),
            res.text().await.unwrap_or_default(),
        )));
    }

    let bytes = res.bytes().await.map_err(TinyPngError::from)?;
    fs::write(path, &bytes).await.map_err(TinyPngError::from)?;

    Ok(bytes.len() as u64)
}

#[pyfunction]
fn rust_sleep(py: Python) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async {
        tokio::time::sleep(std::time::Duration::from_secs(10)).await;
        Ok(())
    })
}

#[pyfunction]
fn compress_image(py: Python,key:String,from:String,to:String) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async {
        println!("start compress image:{} {} {}", key, from, to);
        let result = compress_file(key, from, to).await?;
        Ok(Python::with_gil(|py| [result.0,result.1].into_py(py)))
    })
}


/// A Python module implemented in Rust.
#[pymodule]
fn tinypng_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_sleep, m)?)?;
    m.add_function(wrap_pyfunction!(compress_image, m)?)?;
    Ok(())
}
