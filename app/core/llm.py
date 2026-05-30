import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def safe_llm(prompt: str):
    try:
        return client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            timeout=5  # 🔥 กันค้าง
        ).choices[0].message.content

    except Exception:
        return "fallback: no llm response"