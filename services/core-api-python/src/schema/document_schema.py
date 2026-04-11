from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ExtractedDocument(BaseModel):
    """
    Data Contract สำหรับเอกสารที่ผ่านการสกัดข้อมูล (OCR/AI) เสร็จสิ้นแล้ว
    ข้อมูลนี้จะถูกส่งต่อไปยัง Rust (Actix) เพื่อบันทึกลง Database
    """

    filename: str = Field(
        ...,
        description="ชื่อไฟล์ต้นฉบับ",
        example="invoice_001.pdf"
    )

    extracted_text: str = Field(
        ...,
        description="ข้อความทั้งหมดที่สกัดได้จากรูปภาพ",
        min_length=1 # บังคับว่าต้องมีข้อความอย่างน้อย 1 ตัวอักษร
    )

    confidence_score: float = Field(
        ...,
        description="ระดับความมั่นใจของ AI ในการสกัดข้อมูล (0.0 ถึง 1.0)",
        ge=0.0, # Greater than or equal to 0.0
        le=1.0  # Less than or equal to 1.0
    )

    language: Optional[str] = Field(
        default="tha",
        description="ภาษาหลักของเอกสาร (อ้างอิงรหัส Tesseract เช่น tha, eng)"
    )

    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="ข้อมูลอ้างอิงอื่นๆ เพิ่มเติม (เช่น ขนาดภาพ, ประเภทไฟล์)"
    )