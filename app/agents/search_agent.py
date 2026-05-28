from app.agents.llm import build_gemini_llm
from langchain_core.messages import HumanMessage

def search_node(state: dict) -> dict:
    llm = build_gemini_llm(512)

    res = llm.invoke([HumanMessage(content=state["user_input"])])

    return {
        **state,
        "search_results": [],
        "final_response": res.content
    }