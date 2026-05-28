from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import get_settings
import re

settings = get_settings()

# DEBUG: ใส่ Gemini API key ตรงนี้ชั่วคราว
# เอา key จาก https://aistudio.google.com/app/apikey
DIRECT_GEMINI_KEY = "PASTE_YOUR_REAL_GEMINI_KEY_HERE"

def build_gemini_llm(max_tokens=512):
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=DIRECT_GEMINI_KEY,
        temperature=0.3,
        max_output_tokens=max_tokens,
        timeout=settings.llm_timeout_seconds,
    )

def clean_json_response(text: str) -> str:
    text = text.strip()

    # ลบ markdown block
    text = re.sub(r"^```json", "", text)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    return text.strip()