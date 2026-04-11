from abc import ABC, abstractmethod
import httpx
from src.schema.document_schema import ExtractedDocument

class DataEnginePort(ABC):
    """
    Interface (Port): กำหนดพฤติกรรมมาตรฐานสำหรับการส่งข้อมูลไปยังระบบฐานข้อมูล
    """
    @abstractmethod
    async def send_document_data(self, document: ExtractedDocument) -> bool:
        pass

class ActixHttpClientAdapter(DataEnginePort):
    """
    Concrete Adapter: จัดการเรื่อง HTTP Protocol, Timeout, และ Serialization
    """
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.endpoint = f"{self.base_url}/api/v1/documents"

    async def send_document_data(self, document: ExtractedDocument) -> bool:
        """
        แปลงข้อมูล Pydantic เป็น JSON และส่งผ่าน HTTP POST
        """
        # Pydantic รุ่น v2 ใช้ model_dump() ในการแปลงเป็น Dictionary
        payload = document.model_dump()

        try:
            # ใช้ AsyncClient เพื่อไม่ให้บล็อกการทำงานของ FastAPI
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(self.endpoint, json=payload)

                # หาก Actix ตอบกลับด้วย Status Code 2xx ถือว่าสำเร็จ
                response.raise_for_status()
                return True

        except httpx.HTTPError as exc:
            # ในระบบจริง ควรมีการบันทึก (Logging) ข้อผิดพลาดที่นี่
            print(f"Failed to send data to Data Engine (Rust): {exc}")
            return False