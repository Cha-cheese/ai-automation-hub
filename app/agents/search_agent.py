def search_node(state: dict):
    return {
        **state,
        "search_results": [
            "Germany AI investment increasing in 2026",
            "EU automation adoption rising"
        ],
        "intent": "search",
        "final_response": "🔍 Search completed (production mock safe)"
    }