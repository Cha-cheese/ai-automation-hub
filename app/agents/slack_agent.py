from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.core.config import get_settings
from app.core.errors import safe_error_message


settings = get_settings()


def slack_node(state: dict) -> dict:
    summary = state.get("summary", "No summary available.")
    category = state.get("category", "normal")

    emoji = "🚨" if category == "urgent" else "📬"

    message = f"{emoji} *Email Summary*\n\n{summary}"

    if settings.demo_mode:
        return {
            **state,
            "slack_sent": True,
            "final_response": f"Demo Slack message:\n\n{message}"
        }

    if not settings.slack_bot_token:
        return {
            **state,
            "slack_sent": False,
            "final_response": (
                f"{summary}\n\n"
                "SLACK_BOT_TOKEN is missing."
            )
        }

    try:
        client = WebClient(
            token=settings.slack_bot_token,
            timeout=10
        )

        response = client.chat_postMessage(
            channel=settings.slack_default_channel,
            text=message,
            mrkdwn=True
        )

        return {
            **state,
            "slack_sent": True,
            "final_response": (
                f"✅ Summary sent to Slack "
                f"{settings.slack_default_channel}"
            )
        }

    except SlackApiError as e:
        return {
            **state,
            "slack_sent": False,
            "error": safe_error_message(e),
            "final_response": (
                f"{summary}\n\n"
                f"Slack error: {e.response['error']}"
            )
        }

    except Exception as e:
        return {
            **state,
            "slack_sent": False,
            "error": safe_error_message(e),
            "final_response": summary
        }