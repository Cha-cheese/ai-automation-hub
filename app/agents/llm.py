import os
from langchain_google_genai import ChatGoogleGenerativeAI


def build_gemini_llm(max_tokens=256):
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return None

    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.3,
        max_output_tokens=max_tokens,
    )