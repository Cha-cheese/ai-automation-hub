from app.core.google_client import get_gmail_service

def gmail_agent(user_input: str):

    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for msg in messages:
        data = service.users().messages().get(
            userId="me",
            id=msg["id"]
        ).execute()

        emails.append(data.get("snippet", ""))

    return {
        "emails": emails,
        "source": "gmail_real"
    }