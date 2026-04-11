use actix_web::{web, HttpResponse, Responder};
use sqlx::{Pool, Postgres};
use crate::models::document_dto::ExtractedDocumentDto;
use crate::repositories::document_repo::DocumentRepository;

/// Handler สำหรับรับข้อมูลที่สกัดมาจาก Python และบันทึกลง PostgreSQL
pub async fn receive_document(
    // 1. Extractor: ดึง Database Pool ที่แชร์ไว้ใน Application State
    pool: web::Data<Pool<Postgres>>,
    // 2. Extractor: ดึงและถอดรหัส JSON Payload
    document: web::Json<ExtractedDocumentDto>,
) -> impl Responder {

    // ดึงข้อมูลออกจาก Wrapper
    let doc_data = document.into_inner();

    // 3. สร้าง Repository โดยส่ง Connection Pool เข้าไป
    // การใช้ get_ref().clone() เป็นการคัดลอกตัวชี้ (Reference) ซึ่งใช้ทรัพยากรน้อยมาก
    let repo = DocumentRepository::new(pool.get_ref().clone());

    // 4. สั่งบันทึกข้อมูลและจัดการผลลัพธ์ด้วย Pattern Matching
    match repo.save_document(&doc_data).await {
        Ok(_) => {
            // กรณีสำเร็จ: พิมพ์ Log และคืนค่า HTTP 201 Created
            println!("[Rust] Successfully saved document '{}' to PostgreSQL.", doc_data.filename);

            HttpResponse::Created().json(serde_json::json!({
                "status": "success",
                "message": "Data Engine successfully saved the document",
                "filename": doc_data.filename
            }))
        }
        Err(e) => {
            // กรณีล้มเหลว: พิมพ์ Error Log และคืนค่า HTTP 500 Internal Server Error
            eprintln!("[Rust] Database Error: {:?}", e);

            HttpResponse::InternalServerError().json(serde_json::json!({
                "status": "error",
                "message": "Failed to persist document data in the database"
            }))
        }
    }
}