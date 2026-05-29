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
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        res = requests.post(url, json=payload, timeout=30)
        data = res.json()

        # 🔥 DEBUG (สำคัญมาก)
        print("GEMINI RESPONSE:", data)

        # ✅ SAFE CHECK (กัน crash 100%)
        if "candidates" not in data:
            return f"[GEMINI ERROR]: {data}"

        if not data["candidates"]:
            return f"[GEMINI EMPTY RESPONSE]: {data}"

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"[REQUEST ERROR]: {str(e)}"