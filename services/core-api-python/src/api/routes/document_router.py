from fastapi import APIRouter, UploadFile, File, Depends
from src.services.document_processor import DocumentProcessorService
from src.api.dependencies import get_document_processor

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/process")
async def process_document(
    file: UploadFile = File(...),
    processor: DocumentProcessorService = Depends(get_document_processor)
):
    """
    รับไฟล์รูปภาพ (Multipart/Form-Data) จากผู้ใช้งาน
    และส่งต่อให้ Service Layer จัดการ
    """
    # โยนภาระการทำงานไปที่ Business Logic ทันที
    result = await processor.process_upload(file)

    return {
        "message": "Document processed successfully",
        "data": result
    }