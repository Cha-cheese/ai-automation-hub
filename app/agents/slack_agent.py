from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.core.config import get_settings

settings = get_settings()
slack_client = WebClient(token=settings.slack_bot_token)

def slack_node(state: dict) -> dict:
    summary = state.get("summary", "No summary available.")
    category = state.get("category", "normal")
    channel = settings.slack_default_channel
    
    emoji = "🚨" if category == "urgent" else "📬"
    message = f"{emoji} *Email Summary*\n{summary}"
    
    try:
        slack_client.chat_postMessage(channel=channel, text=message, mrkdwn=True)
        return {**state, "slack_sent": True, "final_response": f"Summary sent to Slack {channel}"}
    except SlackApiError as e:
        return {**state, "slack_sent": False, "error": str(e), "final_response": summary}