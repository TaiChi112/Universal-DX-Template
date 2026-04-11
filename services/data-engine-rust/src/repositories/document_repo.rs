use sqlx::{Pool, Postgres};
use crate::models::document_dto::ExtractedDocumentDto;

pub struct DocumentRepository {
    pool: Pool<Postgres>,
}

impl DocumentRepository {
    pub fn new(pool: Pool<Postgres>) -> Self {
        Self { pool }
    }

    /// บันทึกข้อมูลเอกสารลง PostgreSQL
    pub async fn save_document(&self, doc: &ExtractedDocumentDto) -> Result<(), sqlx::Error> {
        // ใช้ runtime query เพื่อหลีกเลี่ยงการผูกติดกับ SQLx offline artifacts ตอน compile
        sqlx::query(
            r#"
            INSERT INTO documents (filename, extracted_text, confidence_score, language)
            VALUES ($1, $2, $3, $4)
            "#,
        )
        .bind(&doc.filename)
        .bind(&doc.extracted_text)
        .bind(doc.confidence_score)
        .bind(&doc.language)
        .execute(&self.pool)
        .await?;

        Ok(())
    }
}
