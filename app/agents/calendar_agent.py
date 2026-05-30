from app.core.google_client import get_calendar_service

def calendar_agent(user_input: str):

    service = get_calendar_service()

    event = {
        "summary": "AI Scheduled Meeting",
        "start": {
            "dateTime": "2026-05-30T10:00:00+07:00"
        },
        "end": {
            "dateTime": "2026-05-30T10:30:00+07:00"
        }
    }

    result = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return {
        "status": "created",
        "event_link": result.get("htmlLink")
    }

from googleapiclient.discovery import build
from app.core.google_client import get_creds

def get_calendar_service():
    creds = get_creds()
    return build("calendar", "v3", credentials=creds)


# ✅ ฟังก์ชันที่ worker เรียก
def create_event(task: str):

    service = get_calendar_service()

    event = {
        "summary": "AI Scheduled Meeting",
        "description": task,
        "start": {
            "dateTime": "2026-05-29T10:00:00+07:00",
            "timeZone": "Asia/Bangkok",
        },
        "end": {
            "dateTime": "2026-05-29T10:30:00+07:00",
            "timeZone": "Asia/Bangkok",
        },
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return created_event.get("htmlLink")