import os
from google import genai


def build_model():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    client = genai.Client(api_key=api_key)

    return client