from abc import ABC, abstractmethod
import io
# สมมติฐานว่ามีการติดตั้งไลบรารีเหล่านี้ใน requirements.txt
# import pytesseract
# from PIL import Image
# from pythainlp.tokenize import word_tokenize

class OcrEnginePort(ABC):
    """
    Interface (Port): กำหนดพฤติกรรมมาตรฐานที่ระบบ OCR ต้องมี
    Business Logic จะรู้จักและเรียกใช้ผ่านคลาสนี้เท่านั้น
    """
    @abstractmethod
    def extract_text(self, image_bytes: bytes) -> str:
        pass

class TesseractOcrAdapter(OcrEnginePort):
    """
    Concrete Adapter: ซ่อนความซับซ้อนของการเรียกใช้เครื่องมือจริง
    """
    def __init__(self, language: str = "tha+eng"):
        self.language = language

    def extract_text(self, image_bytes: bytes) -> str:
        """
        แปลงข้อมูลไบต์เป็นรูปภาพ และรันกระบวนการ OCR
        """
        try:
            # 1. ใช้ Pillow (PIL) อ่านรูปภาพจาก Bytes
            # image = Image.open(io.BytesIO(image_bytes))

            # 2. ใช้ Tesseract สกัดข้อความ
            # raw_text = pytesseract.image_to_string(image, lang=self.language)

            # 3. (ทางเลือก) ใช้ PyThaiNLP ช่วยจัดระเบียบข้อความหรือตัดคำ
            # tokens = word_tokenize(raw_text, engine="newmm")
            # refined_text = " ".join(tokens)

            # จำลองผลลัพธ์สำหรับการทดสอบ
            refined_text = "ข้อความจำลองที่ถูกสกัดและผ่านการตัดคำแล้ว"
            return refined_text

        except Exception as e:
            # ควรมีการทำ Logging ในระบบจริง
            raise RuntimeError(f"OCR Engine failed: {str(e)}")