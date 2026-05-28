def search_node(state: dict):
    return {
        **state,
        "search_results": [
            {"title": "AI News", "content": "Germany increases AI investment in 2026"},
        ],
        "final_response": "🔍 AI search completed (mock safe mode)"
    }