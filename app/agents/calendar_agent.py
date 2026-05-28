from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, timedelta
import json
from app.core.config import get_settings

settings = get_settings()

def calendar_node(state: dict):

    try:
        creds = service_account.Credentials.from_service_account_info(
            json.loads(settings.google_service_account_json),
            scopes=["https://www.googleapis.com/auth/calendar"]
        )

        service = build("calendar", "v3", credentials=creds)

        start = datetime.now() + timedelta(days=1)
        end = start + timedelta(hours=1)

        event = service.events().insert(
            calendarId="primary",
            body={
                "summary": "AI Meeting",
                "start": {"dateTime": start.isoformat(), "timeZone": "Asia/Bangkok"},
                "end": {"dateTime": end.isoformat(), "timeZone": "Asia/Bangkok"}
            }
        ).execute()

        return {
            **state,
            "final_response": f"📅 Calendar event created: {event['id']}"
        }

    except Exception as e:
        return {
            **state,
            "final_response": f"Calendar error: {str(e)}"
        }