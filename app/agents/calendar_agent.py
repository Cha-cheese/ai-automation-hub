from datetime import datetime, timedelta

def calendar_node(state: dict):
    now = datetime.now()

    return {
        **state,
        "calendar_event": {
            "title": "Meeting",
            "start": now.isoformat()
        },
        "final_response": f"📅 Meeting scheduled (mock) at {now}"
    }