from datetime import datetime, timedelta


DEMO_EMAILS = [
    {
        "id": "demo-001",
        "from": "anna.schmidt@berlin-logistics.example",
        "subject": "Urgent: invoice approval needed today",
        "snippet": "Please approve invoice EU-2026-104 before 17:00 so finance can release the supplier payment.",
    },
    {
        "id": "demo-002",
        "from": "marco.rossi@talent-partners.example",
        "subject": "Interview schedule for Automation Engineer role",
        "snippet": "The candidate is available tomorrow at 15:00 CET. Please confirm whether the team can join.",
    },
    {
        "id": "demo-003",
        "from": "n8n-updates@example.com",
        "subject": "Workflow run summary",
        "snippet": "Your email-to-slack automation completed 24 runs this week with no failed executions.",
    },
]


def demo_email_summary() -> str:
    return "\n".join([
        "- Urgent: invoice approval needed today | From: anna.schmidt@berlin-logistics.example | Category: urgent | Finance needs invoice EU-2026-104 approved before 17:00.",
        "- Interview schedule for Automation Engineer role | From: marco.rossi@talent-partners.example | Category: meeting | Candidate is available tomorrow at 15:00 CET.",
        "- Workflow run summary | From: n8n-updates@example.com | Category: info | Weekly automation report shows 24 successful runs.",
    ])


def demo_calendar_event(user_input: str) -> dict:
    start = datetime.now().replace(second=0, microsecond=0) + timedelta(days=1)
    if "3pm" in user_input.lower() or "15" in user_input:
        start = start.replace(hour=15, minute=0)
    else:
        start = start.replace(hour=10, minute=0)

    return {
        "mock": True,
        "title": "Demo meeting",
        "start": start.isoformat(),
        "duration_minutes": 60,
    }


def demo_search_response(query: str) -> str:
    return (
        "Demo research summary:\n"
        "- European companies are adopting agentic workflow tools for customer support, operations, and internal knowledge work.\n"
        "- Strong portfolio signals: clear orchestration graph, visible workflow steps, API timeouts, and production-safe fallbacks.\n"
        "- Recommended next demo angle: show a natural-language request routed to search, email summary, calendar scheduling, and Slack notification.\n\n"
        f"Query handled: {query}\n"
        "_Demo mode uses sample results. Add TAVILY_API_KEY for live web search._"
    )
