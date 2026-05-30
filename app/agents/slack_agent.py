import os
import requests


def slack_agent(text: str):

    webhook = os.getenv(
        "SLACK_WEBHOOK_URL"
    )

    if not webhook:

        return {
            "status": "missing webhook"
        }

    try:

        requests.post(
            webhook,
            json={"text": text},
            timeout=10
        )

        return {
            "status": "sent"
        }

    except Exception as e:

        return {
            "status": "error",
            "error": str(e)
        }