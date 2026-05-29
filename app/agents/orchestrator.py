import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")


def automation_graph(state):

    user_input = state.get("user_input", "")

    try:

        response = model.generate_content(user_input)

        return {
            "result": response.text,
            "intent": "success"
        }

    except Exception as e:

        print("LLM ERROR:", repr(e))

        return {
            "result": f"[AI ERROR] {str(e)}",
            "intent": "error"
        }