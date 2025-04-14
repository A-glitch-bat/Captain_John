use axum::{Router, routing::get};
use std::{net::SocketAddr, fs};
use axum::response::Html;

async fn serve_html() -> Html<String> {
    let html_content = fs::read_to_string("index.html").unwrap_or_else(|_| "<h1>Failed to load HTML</h1>".to_string());
    Html(html_content)
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/", get(serve_html));

    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    println!("Listening on http://{}", addr);

    axum::serve(tokio::net::TcpListener::bind(addr).await.unwrap(), app)
        .await
        .unwrap();
}
