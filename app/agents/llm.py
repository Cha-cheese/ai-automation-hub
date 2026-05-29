import os
import requests


def call_ai(prompt: str):

    api_key = os.getenv("GEMINI_API_KEY")

    # 🔥 ถ้าไม่มี key → ไม่ crash
    if not api_key:
        return f"[MOCK MODE] {prompt}"

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    headers = {
        "Content-Type": "application/json"
    }

    params = {"key": api_key}

    body = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        res = requests.post(url, headers=headers, params=params, json=body, timeout=20)
        data = res.json()

        # 🔥 SAFE PARSE (ไม่พังแน่นอน)
        if "candidates" in data:
            return data["candidates"][0]["content"]["parts"][0]["text"]

        return f"[AI RESPONSE RAW]: {data}"

    except Exception as e:
        return f"[AI FALLBACK]: {str(e)}"