from langchain_core.messages import HumanMessage, SystemMessage
from app.agents.llm import build_gemini_llm, clean_json_response
from app.agents.demo_data import demo_email_summary
from app.core.config import get_settings
from app.core.errors import safe_error_message

settings = get_settings()

SUMMARIZE_PROMPT = """Summarize these emails briefly. For each email output:
- Subject, From, Category (urgent/meeting/info/spam), 1-sentence summary.
Format as JSON array. No markdown, no code blocks, only raw JSON."""

def summarizer_node(state: dict) -> dict:
    emails = state.get("email_data", {}).get("emails", [])
    if not emails:
        error = state.get("error")
        note = f"\n\nSetup note: {error}" if error else ""
        return {**state, "summary": f"No emails to summarize.{note}", "category": "none"}

    if settings.demo_mode:
        return {**state, "summary": demo_email_summary(), "category": "urgent"}

    try:
        llm = build_gemini_llm(max_tokens=512)
        response = llm.invoke([
            SystemMessage(content=SUMMARIZE_PROMPT),
            HumanMessage(content=str(emails))
        ])
        import json
        summaries = json.loads(clean_json_response(response.content))
        urgent = [s for s in summaries if s.get("category") == "urgent"]
        return {
            **state,
            "summary": response.content,
            "category": "urgent" if urgent else "normal"
        }
    except Exception as e:
        fallback = "\n".join(
            f"- {email.get('subject', '(no subject)')} from {email.get('from', 'unknown')}: {email.get('snippet', '')}"
            for email in emails
        )
        return {**state, "summary": fallback, "category": "normal", "error": safe_error_message(e)}
