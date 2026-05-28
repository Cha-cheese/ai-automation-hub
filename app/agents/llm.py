import os
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import get_settings

settings = get_settings()

def build_gemini_llm(max_tokens=256):
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_api_key,
        temperature=0.3,
        max_output_tokens=max_tokens,
    )

def clean_json_response(text: str):
    return text.replace("```", "").strip()