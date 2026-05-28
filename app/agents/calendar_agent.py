from datetime import datetime

def calendar_node(state: dict):
    return {
        **state,
        "calendar_event": {
            "title": "Meeting",
            "time": datetime.now().isoformat()
        },
        "intent": "calendar",
        "final_response": "📅 Calendar event created (Level 4 mock)"
    }