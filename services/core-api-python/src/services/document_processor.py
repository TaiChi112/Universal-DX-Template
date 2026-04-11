from fastapi import UploadFile, HTTPException
from src.schema.document_schema import ExtractedDocument
from src.infrastructure.ocr_engine import OcrEnginePort
from src.infrastructure.rust_client import DataEnginePort

class DocumentProcessorService:
    def __init__(self, ocr_engine: OcrEnginePort, data_engine: DataEnginePort):
        """
        รับ Adapters ทั้งสองตัวเข้ามาผ่าน Constructor (Dependency Injection)
        """
        self.ocr_engine = ocr_engine
        self.data_engine = data_engine

    async def process_upload(self, file: UploadFile) -> ExtractedDocument:
        # 1. สกัดข้อความ (Delegate to OCR Adapter)
        file_content = await file.read()
        extracted_text = self.ocr_engine.extract_text(file_content)

        # 2. ตรวจสอบความถูกต้องของข้อมูล (Data Validation)
        validated_data = ExtractedDocument(
            filename=file.filename,
            extracted_text=extracted_text,
            confidence_score=0.92,
            metadata={"processed_by": "core-api-python"}
        )

        # 3. ส่งข้อมูลข้ามบริการ (Delegate to HTTP Client Adapter)
        is_success = await self.data_engine.send_document_data(validated_data)

        if not is_success:
            # หากส่งข้อมูลไม่สำเร็จ แจ้งกลับไปยัง Presentation Layer
            raise HTTPException(status_code=502, detail="Failed to communicate with Data Engine")

        return validated_data