from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import get_settings

settings = get_settings()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=settings.google_api_key,
    max_tokens=512,
)

def search_node(state: dict) -> dict:
    # Try Tavily if key exists
    if settings.tavily_api_key:
        try:
            from tavily import TavilyClient
            tavily = TavilyClient(api_key=settings.tavily_api_key)
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
            pass

    # Fallback: Gemini answers from its own knowledge
    response = llm.invoke([
        SystemMessage(content="Answer the user's question helpfully and concisely. Note that you're answering from training data, not live search."),
        HumanMessage(content=state["user_input"])
    ])
    return {
        **state,
        "search_results": [],
        "final_response": response.content + "\n\n_Note: Connect Tavily API for live web search results._"
    }