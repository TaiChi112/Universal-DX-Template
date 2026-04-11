import pytest
import io
from fastapi import UploadFile

from src.services.document_processor import DocumentProcessorService
from src.infrastructure.ocr_engine import OcrEnginePort
from src.infrastructure.rust_client import DataEnginePort
from src.schema.document_schema import ExtractedDocument

# 1. สร้าง Mock สำหรับ OCR Engine
class MockOcrEngine(OcrEnginePort):
    def extract_text(self, image_bytes: bytes) -> str:
        # ไม่ต้องประมวลผลภาพจริง คืนค่าข้อความจำลองกลับไปเลย
        return "Unit Test Extracted Text"

# 2. สร้าง Mock สำหรับ Data Engine (Rust HTTP Client)
class MockDataEngine(DataEnginePort):
    def __init__(self):
        self.was_called = False # ตัวแปรเพื่อตรวจสอบว่าฟังก์ชันนี้ถูกเรียกใช้งานจริงหรือไม่

    async def send_document_data(self, document: ExtractedDocument) -> bool:
        self.was_called = True
        return True # จำลองว่าส่งข้อมูลสำเร็จเสมอ

# ต้องใช้ Decorator นี้เพราะ Business Logic ของเราเป็น Asynchronous (async def)
@pytest.mark.asyncio
async def test_process_upload_success():
    # ==========================================
    # 1. ARRANGE: เตรียมสภาพแวดล้อมและข้อมูลทดสอบ
    # ==========================================
    mock_ocr = MockOcrEngine()
    mock_data_engine = MockDataEngine()

    # Inject Mock เข้าไปใน Service แทนของจริง
    processor = DocumentProcessorService(ocr_engine=mock_ocr, data_engine=mock_data_engine)

    # จำลองไฟล์รูปภาพที่ถูกอัปโหลดเข้ามาผ่าน FastAPI
    fake_file_content = b"fake image bytes"
    fake_upload_file = UploadFile(
        filename="test_invoice.png",
        file=io.BytesIO(fake_file_content)
    )

    # ==========================================
    # 2. ACT: รันฟังก์ชันที่ต้องการทดสอบ
    # ==========================================
    result = await processor.process_upload(fake_upload_file)

    # ==========================================
    # 3. ASSERT: ตรวจสอบความถูกต้องของผลลัพธ์
    # ==========================================
    # ตรวจสอบว่าผลลัพธ์ที่ได้ตรงตาม Pydantic Schema และ Mock Data หรือไม่
    assert result.filename == "test_invoice.png"
    assert result.extracted_text == "Unit Test Extracted Text"
    assert result.confidence_score == pytest.approx(0.92)

    # ตรวจสอบว่า Service มีการสั่งให้ Adapter ส่งข้อมูลไปหา Rust หรือไม่
    assert mock_data_engine.was_called is True

from fastapi import HTTPException

# ==========================================
# 1. สร้าง Mock สำหรับกรณีล้มเหลว (Sad Path Mock)
# ==========================================
class MockDataEngineFailing(DataEnginePort):
    async def send_document_data(self, document: ExtractedDocument) -> bool:
        """
        จำลองสถานการณ์ที่เซิร์ฟเวอร์ Rust ล่ม หรือ Network ตัดขาด
        """
        return False

# ==========================================
# 2. Test Case: กรณีที่ส่งข้อมูลข้ามบริการไม่สำเร็จ
# ==========================================
@pytest.mark.asyncio
async def test_process_upload_rust_service_down():
    # 1. ARRANGE: เตรียมสภาพแวดล้อม
    mock_ocr = MockOcrEngine() # OCR ทำงานสำเร็จตามปกติ
    mock_data_engine_failing = MockDataEngineFailing() # แต่ส่งข้อมูลไป Rust ล้มเหลว

    # Inject ตัวจำลองที่ล้มเหลวเข้าไปใน Service
    processor = DocumentProcessorService(ocr_engine=mock_ocr, data_engine=mock_data_engine_failing)

    fake_upload_file = UploadFile(
        filename="test_invoice.png",
        file=io.BytesIO(b"fake image bytes")
    )

    # 2. ACT & ASSERT: ลงมือทำและตรวจสอบ Exception ในคราวเดียว
    # ใช้ pytest.raises เพื่อดักจับ HTTPException ที่ถูกโยนออกมา
    with pytest.raises(HTTPException) as exc_info:
        await processor.process_upload(fake_upload_file)

    # 3. ตรวจสอบรายละเอียดของ Exception (Validation)
    # ต้องมั่นใจว่าระบบคืนค่า Status 502 (Bad Gateway) ไม่ใช่ 500 (Internal Server Error)
    assert exc_info.value.status_code == 502
    assert exc_info.value.detail == "Failed to communicate with Data Engine"