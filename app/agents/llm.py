import os

# optional Gemini
try:
    import google.generativeai as genai
except:
    genai = None


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if genai and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    def generate(self, prompt: str) -> str:
        try:
            if self.model:
                res = self.model.generate_content(prompt)
                return res.text
        except Exception:
            pass

        # fallback (safe mode)
        return f"[MOCK LLM RESPONSE] {prompt[:50]}"


llm_client = LLMClient()