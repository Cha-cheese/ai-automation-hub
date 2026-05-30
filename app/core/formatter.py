def format_response(result: dict):

    gmail = result.get("data", {}).get("gmail", {})
    slack = result.get("data", {}).get("slack", {})
    calendar = result.get("data", {}).get("calendar", {})

    emails = gmail.get("emails", [])

    formatted = {
        "🧠 Intent": result.get("intent"),
        "📧 Gmail Summary": [
            email[:120] + "..." if len(email) > 120 else email
            for email in emails
        ],
        "💬 Slack Status": slack.get("status", "not sent"),
        "📅 Calendar": calendar.get("status", "not created"),
        "🔗 Event Link": calendar.get("event_link") or calendar.get("event"),
    }

    return formatted