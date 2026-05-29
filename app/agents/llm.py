import os
import requests

API_KEY = os.getenv("GEMINI_API_KEY")


def call_gemini(prompt: str):

    if not API_KEY:
        return "[ERROR] Missing GEMINI_API_KEY"

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-1.5-flash:generateContent?key={API_KEY}"
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

        print("RAW GEMINI RESPONSE:", data)

        # 🔥 SAFE MODE (กันพัง 100%)
        candidates = data.get("candidates")

        if not candidates:
            return f"[GEMINI ERROR RAW]: {data}"

        content = candidates[0].get("content", {})
        parts = content.get("parts", [])

        if not parts:
            return f"[GEMINI EMPTY PARTS]: {data}"

        return parts[0].get("text", str(data))

    except Exception as e:
        return f"[REQUEST FAILED]: {str(e)}"