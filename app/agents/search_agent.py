from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import get_settings
from app.core.errors import safe_error_message
from app.agents.llm import build_gemini_llm

settings = get_settings()

def search_node(state: dict) -> dict:
    # Try Tavily if key exists
    if settings.tavily_api_key:
        try:
            import httpx
            response = httpx.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": settings.tavily_api_key,
                    "query": state["user_input"],
                    "max_results": 5,
                },
                timeout=settings.tavily_timeout_seconds,
            )
            response.raise_for_status()
            results = response.json()
            sources = results.get("results", [])
            context = "\n\n".join([f"Source: {r['url']}\n{r['content']}" for r in sources])

            llm = build_gemini_llm(max_tokens=512)
            response = llm.invoke([
                SystemMessage(content="Answer the question using the provided web search results. Be concise and cite sources."),
                HumanMessage(content=f"Question: {state['user_input']}\n\nSearch Results:\n{context}")
            ])
            return {
                **state,
                "search_results": sources,
                "final_response": response.content
            }
        except Exception as e:
            return {
                **state,
                "search_results": [],
                "error": safe_error_message(e),
                "final_response": (
                    "Live web search is not available right now. Check TAVILY_API_KEY/network access, "
                    "then try again. The backend returned instead of waiting forever."
                )
            }

    # Fallback: Gemini answers from its own knowledge
    try:
        llm = build_gemini_llm(max_tokens=512)
        response = llm.invoke([
            SystemMessage(content="Answer the user's question helpfully and concisely. Note that you're answering from training data, not live search."),
            HumanMessage(content=state["user_input"])
        ])
        final_response = response.content + "\n\n_Note: Connect Tavily API for live web search results._"
    except Exception as e:
        final_response = (
            "Search agent received your request, but neither Tavily nor Gemini is available. "
            "Set TAVILY_API_KEY for live search and GOOGLE_API_KEY for synthesis."
        )
        return {**state, "search_results": [], "error": safe_error_message(e), "final_response": final_response}

    return {**state, "search_results": [], "final_response": final_response}
