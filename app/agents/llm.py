from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings


def build_gemini_llm(max_tokens: int = 512) -> ChatGoogleGenerativeAI:
    settings = get_settings()
    if not settings.google_api_key:
        raise RuntimeError("GOOGLE_API_KEY is not configured.")

    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_api_key,
        max_tokens=max_tokens,
        timeout=settings.llm_timeout_seconds,
        max_retries=1,
    )


def clean_json_response(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1].strip()
        if text.startswith("json"):
            text = text[4:].strip()
    return text
