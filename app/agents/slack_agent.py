import os
import requests

def slack_agent(message: str):

    webhook = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook:
        return {"status": "missing webhook"}

    payload = {"text": message}

    requests.post(webhook, json=payload)

    return {"status": "sent"}