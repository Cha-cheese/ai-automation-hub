def slack_node(state: dict):
    msg = state.get("final_response", "")

    return {
        **state,
        "slack_sent": True,
        "final_response": f"📨 Slack delivered:\n{msg}"
    }