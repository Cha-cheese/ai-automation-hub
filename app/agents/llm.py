from dataclasses import dataclass

import httpx

from app.core.config import get_settings


@dataclass
class LLMResponse:
    content: str


class GeminiRestLLM:
    def __init__(self, max_tokens: int = 512):
        self.settings = get_settings()
        self.max_tokens = max_tokens
        if not self.settings.google_api_key:
            raise RuntimeError("GOOGLE_API_KEY is not configured.")

    def invoke(self, messages: list) -> LLMResponse:
        system_parts = []
        user_parts = []

        for message in messages:
            content = getattr(message, "content", str(message))
            message_type = getattr(message, "type", "")
            if message_type == "system":
                system_parts.append(content)
            else:
                user_parts.append(content)

        prompt = "\n\n".join(system_parts + user_parts)
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.settings.gemini_model}:generateContent"
        )
        response = httpx.post(
            url,
            params={"key": self.settings.google_api_key},
            json={
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": self.max_tokens},
            },
            timeout=self.settings.llm_timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        candidates = data.get("candidates", [])
        if not candidates:
            raise RuntimeError("Gemini returned no candidates.")

        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in parts).strip()
        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return LLMResponse(content=text)


def build_gemini_llm(max_tokens: int = 512) -> GeminiRestLLM:
    settings = get_settings()
    if not settings.google_api_key:
        raise RuntimeError("GOOGLE_API_KEY is not configured.")

    return GeminiRestLLM(max_tokens=max_tokens)


def clean_json_response(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1].strip()
        if text.startswith("json"):
            text = text[4:].strip()
    return text
