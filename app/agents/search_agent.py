from tavily import TavilyClient
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import get_settings

settings = get_settings()
tavily = TavilyClient(api_key=settings.tavily_api_key)
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=settings.anthropic_api_key,
    max_tokens=512,
)

def search_node(state: dict) -> dict:
    try:
        results = tavily.search(query=state["user_input"], max_results=5)
        sources = results.get("results", [])
        context = "\n\n".join([f"Source: {r['url']}\n{r['content']}" for r in sources])
        
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
        return {**state, "error": str(e), "final_response": str(e)}