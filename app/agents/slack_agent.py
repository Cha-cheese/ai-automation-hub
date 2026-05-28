from slack_sdk import WebClient
from app.core.config import get_settings

settings = get_settings()

def slack_node(state: dict):

    try:
        client = WebClient(token=settings.slack_bot_token)

        client.chat_postMessage(
            channel="#ai",
            text=f"🤖 AI Update: {state.get('user_input')}"
        )

        return {
            **state,
            "final_response": "✅ Slack sent successfully"
        }

    except Exception as e:
        return {
            **state,
            "final_response": f"Slack error: {str(e)}"
        }