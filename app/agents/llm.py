import os
import requests

API_KEY = os.getenv("GEMINI_API_KEY")


def call_gemini(prompt: str):

    if not API_KEY:
        return "[ERROR] Missing GEMINI_API_KEY"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        res = requests.post(url, json=payload, timeout=30)
        data = res.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"[GEMINI REST ERROR]: {str(e)}"