import os
from src.services.document_processor import DocumentProcessorService
from src.infrastructure.ocr_engine import TesseractOcrAdapter, OcrEnginePort
from src.infrastructure.rust_client import ActixHttpClientAdapter, DataEnginePort

# 1. สร้าง Singleton สำหรับ OCR (เพื่อประหยัดหน่วยความจำ)
_ocr_adapter_instance = TesseractOcrAdapter(language="tha+eng")

def get_ocr_engine() -> OcrEnginePort:
    return _ocr_adapter_instance

# 2. สร้าง Singleton สำหรับ HTTP Client
# ใช้ URL ตามที่กำหนดไว้ใน docker-compose.yml
RUST_SERVICE_URL = os.getenv("RUST_SERVICE_URL", "http://localhost:8080")
_data_engine_instance = ActixHttpClientAdapter(base_url=RUST_SERVICE_URL)

def get_data_engine() -> DataEnginePort:
    return _data_engine_instance

# 3. ประกอบร่าง Service (The Factory)
def get_document_processor() -> DocumentProcessorService:
    ocr_engine = get_ocr_engine()
    data_engine = get_data_engine()

    # ฉีด Adapter ทั้งสองตัวเข้าไปใน Service
    return DocumentProcessorService(
        ocr_engine=ocr_engine,
        data_engine=data_engine
    )