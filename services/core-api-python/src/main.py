from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import document_router

def create_app() -> FastAPI:
    """
    Application Factory: ฟังก์ชันสำหรับสร้างและตั้งค่า FastAPI
    """
    app = FastAPI(
        title="Core API (Intelligent Document Processing)",
        description="API สำหรับรับเอกสารและส่งต่อให้ระบบ AI วิเคราะห์",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # 1. การตั้งค่าความปลอดภัย (CORS Middleware)
    # อนุญาตให้ระบบอื่น (เช่น Frontend หรือ Actix) สามารถยิง Request เข้ามาได้
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # ในระดับ Production ควรเปลี่ยนเป็น URL ที่อนุญาตเท่านั้น
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. การลงทะเบียน Router (Presentation Layer)
    # เพิ่ม prefix "/api/v1" เพื่อรองรับการทำ Versioning ในอนาคต
    app.include_router(document_router.router, prefix="/api/v1")

    return app

# สร้างออบเจกต์แอปพลิเคชันเพื่อให้ Uvicorn นำไปรัน
app = create_app()

@app.get("/health", tags=["System"])
async def health_check():
    """
    Endpoint พื้นฐานสำหรับตรวจสอบว่าเซิร์ฟเวอร์ยังทำงานปกติหรือไม่
    """
    return {
        "status": "healthy",
        "service": "core-api-python",
        "architecture": "Clean Architecture"
    }