from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import get_settings
import re

settings = get_settings()

def build_gemini_llm(max_tokens=512):
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_api_key,
        temperature=0,
        timeout=settings.llm_timeout_seconds,
    )

def clean_json_response(text: str) -> str:
    text = text.strip()
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    return text.strip()