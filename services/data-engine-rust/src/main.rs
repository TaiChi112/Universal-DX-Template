mod handlers;
mod models;
mod infrastructure;
mod repositories;

use actix_web::{web, App, HttpServer};
use dotenv::dotenv;
use infrastructure::db::{establish_connection, initialize_schema};
use handlers::document_handler::receive_document;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // โหลดไฟล์ .env (หากมี)
    dotenv().ok();

    println!("Starting Data Engine (Rust/Actix) on port 8080...");

    // 1. สร้าง Database Pool เพียงครั้งเดียวเมื่อเปิดเซิร์ฟเวอร์
    let pool = establish_connection().await;

    // 2. สร้าง schema ที่จำเป็น (idempotent) เพื่อรองรับเครื่องใหม่และ CI
    initialize_schema(&pool)
        .await
        .expect("Failed to initialize database schema");

    // 3. ส่ง Pool เข้าไปใน Actix HttpServer
    HttpServer::new(move || {
        App::new()
            // ใช้ web::Data เพื่อแชร์ State ไปให้ทุกๆ Route
            .app_data(web::Data::new(pool.clone()))
            .route("/api/v1/documents", web::post().to(receive_document))
    })
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}