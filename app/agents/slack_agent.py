from slack_sdk import WebClient
from app.core.config import get_settings

settings = get_settings()

def slack_node(state: dict):
    try:
        client = WebClient(token=settings.slack_bot_token)

        client.chat_postMessage(
            channel="#general",
            text=state.get("final_response", "update")
        )

        return {**state, "slack_sent": True}

    except Exception as e:
        return {**state, "slack_sent": False, "error": str(e)}