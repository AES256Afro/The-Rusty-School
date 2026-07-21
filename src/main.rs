//! The Rusty School — web server
//! ============================
//!
//! This little program serves the entire Rusty School website from the
//! `docs/` folder. It is written in 100% standard-library Rust — no
//! external dependencies at all — so `cargo run` starts instantly.
//!
//! It is also a *lesson*: once you finish the curriculum on the site,
//! come back and read this file top to bottom. Everything here is
//! covered in the lessons:
//!
//!   * functions & control flow ......... Lessons 4–5
//!   * ownership & borrowing ............ Lessons 6–7
//!   * structs, enums & `match` ......... Lessons 8–9
//!   * `String` vs `&str` ............... Lesson 10
//!   * `Option`, `Result` and `?` ....... Lessons 9 & 11
//!   * traits (`Display`) ............... Lesson 12
//!   * threads ("fearless concurrency") . Lesson 16
//!   * modules & unit tests ............. Lesson 17
//!
//! Run it with:  cargo run
//! Then open:    http://localhost:7878

use std::fs;
use std::io::{BufRead, BufReader, Write};
use std::net::{TcpListener, TcpStream};
use std::path::PathBuf;
use std::thread;

/// The address the server listens on. 7878 is "RUST" typed on a phone keypad.
const ADDRESS: &str = "127.0.0.1:7878";

/// Where the website lives, relative to where you run `cargo run`.
const SITE_ROOT: &str = "docs";

fn main() {
    // `expect` crashes with a friendly message if the port is taken.
    // You'll learn about `Result` and error handling in Lesson 11.
    let listener = TcpListener::bind(ADDRESS)
        .expect("could not bind to port 7878 — is another server already running?");

    println!("🦀 The Rusty School is open!");
    println!("   Visit  http://{ADDRESS}  in your browser.");
    println!("   Press  Ctrl+C  to stop the server.\n");

    // `incoming()` gives us an iterator of connections (Lesson 14).
    for stream in listener.incoming() {
        match stream {
            // Each connection is handled on its own thread (Lesson 16).
            // `move` hands ownership of `stream` to the thread (Lesson 6).
            Ok(stream) => {
                thread::spawn(move || handle_connection(stream));
            }
            Err(e) => eprintln!("connection failed: {e}"),
        }
    }
}

/// Read one HTTP request from the browser and send back a response.
fn handle_connection(mut stream: TcpStream) {
    let reader = BufReader::new(&stream);

    // The first line of an HTTP request looks like:  GET /learn/index.html HTTP/1.1
    let request_line = match reader.lines().next() {
        Some(Ok(line)) => line,
        _ => return, // The browser hung up early — nothing to do.
    };

    // Split the request line into its three parts.
    let mut parts = request_line.split_whitespace();
    let method = parts.next().unwrap_or("");
    let raw_path = parts.next().unwrap_or("/");

    // This server only ever needs to answer GET requests.
    if method != "GET" {
        respond(&mut stream, "405 Method Not Allowed", "text/plain", b"405");
        return;
    }

    match resolve(raw_path) {
        Some(file_path) => match fs::read(&file_path) {
            Ok(body) => {
                let mime = mime_type(&file_path);
                respond(&mut stream, "200 OK", mime, &body);
            }
            Err(_) => not_found(&mut stream),
        },
        None => not_found(&mut stream),
    }
}

/// Turn a URL path like `/learn/` into a safe file path like `docs/learn/index.html`.
///
/// Returns `None` (Lesson 9!) if the path tries to escape the site folder —
/// requests containing `..` could otherwise read files they shouldn't.
fn resolve(raw_path: &str) -> Option<PathBuf> {
    // Ignore anything after `?` (query strings) or `#` (fragments).
    let path = raw_path.split(['?', '#']).next().unwrap_or("/");

    // Security check: refuse sneaky paths like /../../etc/passwd
    if path.contains("..") {
        return None;
    }

    // Build the path piece by piece, skipping empty segments from `//`.
    let mut file_path = PathBuf::from(SITE_ROOT);
    for segment in path.split('/').filter(|s| !s.is_empty()) {
        file_path.push(segment);
    }

    // `/` or `/learn/` means "give me the index.html in that folder".
    if file_path.is_dir() {
        file_path.push("index.html");
    }

    // Friendly URLs: `/setup` works as well as `/setup.html`.
    if file_path.extension().is_none() {
        file_path.set_extension("html");
    }

    if file_path.is_file() {
        Some(file_path)
    } else {
        None
    }
}

/// Pick the right `Content-Type` header from the file extension so the
/// browser knows whether it received HTML, CSS, an image, and so on.
fn mime_type(path: &PathBuf) -> &'static str {
    // `and_then` and `unwrap_or` are Option helpers — Lesson 9.
    let extension = path.extension().and_then(|e| e.to_str()).unwrap_or("");

    match extension {
        "html" => "text/html; charset=utf-8",
        "css" => "text/css; charset=utf-8",
        "js" => "text/javascript; charset=utf-8",
        "svg" => "image/svg+xml",
        "png" => "image/png",
        "jpg" | "jpeg" => "image/jpeg",
        "ico" => "image/x-icon",
        "json" => "application/json",
        "txt" => "text/plain; charset=utf-8",
        "woff2" => "font/woff2",
        _ => "application/octet-stream",
    }
}

/// Write a complete HTTP response: status line, headers, blank line, body.
fn respond(stream: &mut TcpStream, status: &str, mime: &str, body: &[u8]) {
    let header = format!(
        "HTTP/1.1 {status}\r\nContent-Type: {mime}\r\nContent-Length: {}\r\n\r\n",
        body.len()
    );

    // If the browser disconnected mid-response, there is nobody left to
    // tell — so we deliberately ignore write errors with `.ok()`.
    stream.write_all(header.as_bytes()).ok();
    stream.write_all(body).ok();
}

/// Send a small 404 page. If the site has a custom 404.html, use that.
fn not_found(stream: &mut TcpStream) {
    let body = fs::read(format!("{SITE_ROOT}/404.html")).unwrap_or_else(|_| {
        b"<h1>404 &mdash; page not found</h1><p><a href='/'>Back to The Rusty School</a></p>"
            .to_vec()
    });
    respond(stream, "404 Not Found", "text/html; charset=utf-8", &body);
}

// ---------------------------------------------------------------------------
// Unit tests (Lesson 17). Run them with:  cargo test
// ---------------------------------------------------------------------------
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn html_gets_the_right_mime_type() {
        let path = PathBuf::from("docs/index.html");
        assert_eq!(mime_type(&path), "text/html; charset=utf-8");
    }

    #[test]
    fn unknown_extensions_fall_back_to_octet_stream() {
        let path = PathBuf::from("docs/mystery.xyz");
        assert_eq!(mime_type(&path), "application/octet-stream");
    }

    #[test]
    fn sneaky_paths_are_rejected() {
        assert_eq!(resolve("/../secret.txt"), None);
        assert_eq!(resolve("/learn/../../etc/passwd"), None);
    }

    #[test]
    fn query_strings_are_ignored() {
        // resolve() only returns Some for files that exist on disk,
        // so here we just check it doesn't panic on odd input.
        let _ = resolve("/quiz.html?level=1#top");
    }
}
