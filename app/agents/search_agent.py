import requests
from app.core.config import get_settings

settings = get_settings()

def search_node(state: dict):

    try:
        r = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": settings.tavily_api_key,
                "query": state["user_input"],
                "max_results": 3
            },
            timeout=10
        )

        data = r.json()
        results = data.get("results", [])

        if not results:
            return {
                **state,
                "final_response": "No search results found"
            }

        top = results[0]

        return {
            **state,
            "final_response": f"{top['title']}\n\n{top['content']}"
        }

    except Exception as e:
        return {
            **state,
            "final_response": f"Search error: {str(e)}"
        }