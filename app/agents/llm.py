import os
import google.generativeai as genai


def build_gemini_llm():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        "gemini-1.5-flash"
    )

    return model