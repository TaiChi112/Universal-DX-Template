use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Debug, Deserialize, Serialize)]
pub struct ExtractedDocumentDto {
    pub filename: String,
    pub extracted_text: String,
    pub confidence_score: f64,

    // Option<T> ใน Rust เทียบเท่ากับ Optional[T] ใน Python
    pub language: Option<String>,

    // Value คือประเภทข้อมูลที่รองรับ JSON Object ที่มีโครงสร้างอิสระ (เทียบเท่า Dict[str, Any])
    pub metadata: Option<Value>,
}