from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import get_settings

settings = get_settings()
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=settings.anthropic_api_key,
    max_tokens=512,
)

SUMMARIZE_PROMPT = """Summarize these emails briefly. For each email output:
- Subject, From, Category (urgent/meeting/info/spam), 1-sentence summary.
Format as JSON array. No markdown."""

def summarizer_node(state: dict) -> dict:
    emails = state.get("email_data", {}).get("emails", [])
    if not emails:
        return {**state, "summary": "No emails to summarize.", "category": "none"}
    
    response = llm.invoke([
        SystemMessage(content=SUMMARIZE_PROMPT),
        HumanMessage(content=str(emails))
    ])
    try:
        import json
        summaries = json.loads(response.content)
        urgent = [s for s in summaries if s.get("category") == "urgent"]
        return {
            **state,
            "summary": response.content,
            "category": "urgent" if urgent else "normal"
        }
    except:
        return {**state, "summary": response.content, "category": "normal"}