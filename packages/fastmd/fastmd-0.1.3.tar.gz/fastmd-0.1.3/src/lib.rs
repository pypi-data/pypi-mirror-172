use pyo3::prelude::*;

//use std::io;
//external
use pulldown_cmark::{Parser, Options, html};


#[pyfunction]
fn tohtml(buffer: String) -> PyResult<String>  {

    // Set up options and parser. Strikethroughs are not part of the CommonMark standard
    // and we therefore must enable it explicitly.
    let mut options = Options::empty();
    options.insert(Options::ENABLE_STRIKETHROUGH);
    options.insert(Options::ENABLE_TABLES);
    options.insert(Options::ENABLE_TASKLISTS);
    let parser = Parser::new_ext(&buffer, options);

    // Write to String buffer.
    let mut html_output = String::new();
    html::push_html(&mut html_output, parser);

    Ok(html_output)
}

/// A Python module implemented in Rust.
#[pymodule]
fn fastmd(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(tohtml, m)?)?;
    Ok(())
}


