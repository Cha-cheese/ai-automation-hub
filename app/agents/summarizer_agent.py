from langchain_core.messages import HumanMessage, SystemMessage
from app.agents.llm import build_gemini_llm, clean_json_response

SUMMARIZE_PROMPT = """Summarize these emails briefly. For each email output:
- Subject, From, Category (urgent/meeting/info/spam), 1-sentence summary.
Format as JSON array. No markdown, no code blocks, only raw JSON."""

def summarizer_node(state: dict) -> dict:
    emails = state.get("email_data", {}).get("emails", [])
    if not emails:
        error = state.get("error")
        note = f"\n\nSetup note: {error}" if error else ""
        return {**state, "summary": f"No emails to summarize.{note}", "category": "none"}

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
        return {**state, "summary": fallback, "category": "normal", "error": str(e)}
