import os
from google import genai


def build_model():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("NO GEMINI KEY")
        return None

    return genai.Client(api_key=api_key)