from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import get_settings

settings = get_settings()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=settings.google_api_key,
    max_tokens=512,
)

SUMMARIZE_PROMPT = """Summarize these emails briefly. For each email output:
- Subject, From, Category (urgent/meeting/info/spam), 1-sentence summary.
Format as JSON array. No markdown, no code blocks, only raw JSON."""

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
        text = response.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        summaries = json.loads(text.strip())
        urgent = [s for s in summaries if s.get("category") == "urgent"]
        return {
            **state,
            "summary": response.content,
            "category": "urgent" if urgent else "normal"
        }
    except:
        return {**state, "summary": response.content, "category": "normal"}