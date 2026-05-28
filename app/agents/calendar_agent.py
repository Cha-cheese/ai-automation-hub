from datetime import datetime, timedelta

def calendar_node(state: dict):
    try:
        start = datetime.now() + timedelta(days=1)

        return {
            **state,
            "calendar_event": {
                "title": "Meeting",
                "start": start.isoformat()
            },
            "final_response": f"📅 Meeting scheduled: {start}"
        }

    except Exception as e:
        return {**state, "final_response": str(e)}