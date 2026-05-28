import requests
from app.core.config import get_settings

settings = get_settings()

def search_node(state: dict):

    try:
        r = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": settings.tavily_api_key,
                "query": state["user_input"]
            }
        )

        data = r.json()

        return {
            **state,
            "final_response": data["results"][0]["content"]
        }

    except Exception as e:
        return {
            **state,
            "final_response": f"Search error: {str(e)}"
        }