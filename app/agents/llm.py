import os
import google.generativeai as genai


def build_model():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("NO GEMINI KEY")
        return None

    genai.configure(api_key=api_key)

    # ✅ ใช้ตัวที่มีจริงใน API v1beta
    model = genai.GenerativeModel("gemini-1.5-flash")

    return model