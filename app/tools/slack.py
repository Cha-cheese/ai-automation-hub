import os
import requests

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")


def send_slack(message: str):
    if not SLACK_WEBHOOK:
        return "Slack not configured"

    requests.post(SLACK_WEBHOOK, json={"text": message})

    return "Slack sent successfully"