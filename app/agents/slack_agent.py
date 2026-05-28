from app.core.config import get_settings

settings = get_settings()

def slack_node(state: dict):
    summary = state.get("final_response", "")

    return {
        **state,
        "slack_sent": True,
        "final_response": f"📨 Slack sent:\n{summary}"
    }