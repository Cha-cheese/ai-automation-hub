from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.core.config import get_settings

settings = get_settings()

def slack_node(state: dict) -> dict:
    summary = state.get("summary", "No summary available.")
    category = state.get("category", "normal")
    channel = settings.slack_default_channel
    
    emoji = "🚨" if category == "urgent" else "📬"
    message = f"{emoji} *Email Summary*\n{summary}"

    if not settings.slack_bot_token:
        return {
            **state,
            "slack_sent": False,
            "final_response": f"{summary}\n\n_Note: Set SLACK_BOT_TOKEN to send this summary to Slack._",
        }
    
    try:
        slack_client = WebClient(token=settings.slack_bot_token, timeout=10)
        slack_client.chat_postMessage(channel=channel, text=message, mrkdwn=True)
        return {**state, "slack_sent": True, "final_response": f"Summary sent to Slack {channel}"}
    except SlackApiError as e:
        return {**state, "slack_sent": False, "error": str(e), "final_response": summary}
    except Exception as e:
        return {**state, "slack_sent": False, "error": str(e), "final_response": summary}
