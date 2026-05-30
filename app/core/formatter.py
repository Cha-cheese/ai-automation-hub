def format_response(result):

    # assistant response
    if "message" in result:
        return {
            "type": "assistant",
            "message": result["message"]
        }

    data = result.get("data", {})

    gmail = data.get("gmail", {})
    slack = data.get("slack", {})
    calendar = data.get("calendar", {})

    emails = gmail.get("emails", [])

    return {
        "type": "automation",

        "intent": result.get("intent"),

        "gmail_count": len(emails),

        "gmail_emails": emails,

        "slack_status": slack.get(
            "status",
            "not sent"
        ),

        "calendar_status": calendar.get(
            "status",
            "not created"
        ),

        "event_link": calendar.get(
            "event_link"
        )
    }