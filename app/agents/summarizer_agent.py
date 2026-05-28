def summarizer_node(state: dict):
    text = state.get("user_input", "")

    return {
        **state,
        "summary": f"General request processed: {text}",
        "intent": "general",
        "final_response": f"🤖 Processed request: {text}"
    }