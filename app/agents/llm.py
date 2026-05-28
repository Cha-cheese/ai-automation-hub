from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import get_settings
import json, re

settings = get_settings()

def build_gemini_llm(max_tokens=512):
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_api_key,
        temperature=0.2,
        max_output_tokens=max_tokens,
    )

def clean_json_response(text: str):
    text = text.replace("```json", "").replace("```", "").strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group() if match else text

def safe_json_load(text: str):
    try:
        return json.loads(text)
    except:
        return {"intent": "general_query"}