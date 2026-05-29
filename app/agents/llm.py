import os
import requests


def call_ai(prompt: str):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return f"[MOCK] {prompt}"

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-1.5-flash:generateContent?key={api_key}"
    )

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        res = requests.post(url, json=payload, timeout=30)
        data = res.json()

        if "candidates" not in data:
            return f"[AI ERROR RAW]: {data}"

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"[AI REQUEST ERROR]: {str(e)}"