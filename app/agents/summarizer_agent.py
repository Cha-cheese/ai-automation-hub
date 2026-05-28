def summarizer_node(state: dict):
    return {
        **state,
        "summary": state.get("final_response", "")
    }