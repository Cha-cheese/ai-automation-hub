from app.core.google_client import get_gmail_service


def gmail_agent(user_input: str):

    try:

        service = get_gmail_service()

        results = (
            service.users()
            .messages()
            .list(
                userId="me",
                maxResults=5
            )
            .execute()
        )

        messages = results.get("messages", [])

        emails = []

        for msg in messages:

            detail = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=msg["id"]
                )
                .execute()
            )

            snippet = detail.get(
                "snippet",
                "No content"
            )

            emails.append(snippet)

        return {
            "emails": emails,
            "source": "gmail_real"
        }

    except Exception as e:

        return {
            "emails": [],
            "source": "gmail_error",
            "error": str(e)
        }