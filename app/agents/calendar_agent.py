from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import get_settings
from datetime import datetime, timedelta
import json

settings = get_settings()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=settings.google_api_key,
    max_tokens=256,
)

EXTRACT_PROMPT = f"""Extract meeting details from this text.
Current datetime: {datetime.now().isoformat()}
Return JSON only (no markdown, no code blocks):
{{"title": "", "start_time": "ISO8601", "duration_minutes": 60, "description": ""}}"""

def calendar_node(state: dict) -> dict:
    try:
        response = llm.invoke([
            SystemMessage(content=EXTRACT_PROMPT),
            HumanMessage(content=state["user_input"])
        ])
        text = response.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        event_data = json.loads(text.strip())

        start = datetime.fromisoformat(event_data["start_time"])
        end = start + timedelta(minutes=event_data.get("duration_minutes", 60))

        # Try real Google Calendar if credentials exist
        if settings.google_service_account_json != "{}":
            try:
                from googleapiclient.discovery import build
                from google.oauth2 import service_account
                creds_json = json.loads(settings.google_service_account_json)
                creds = service_account.Credentials.from_service_account_info(
                    creds_json,
                    scopes=["https://www.googleapis.com/auth/calendar"]
                )
                service = build("calendar", "v3", credentials=creds)
                event = {
                    "summary": event_data["title"],
                    "description": event_data.get("description", ""),
                    "start": {"dateTime": start.isoformat(), "timeZone": "Europe/Berlin"},
                    "end": {"dateTime": end.isoformat(), "timeZone": "Europe/Berlin"},
                }
                created = service.events().insert(calendarId="primary", body=event).execute()
                return {
                    **state,
                    "calendar_event": created,
                    "final_response": f"✅ Meeting '{event_data['title']}' scheduled for {start.strftime('%Y-%m-%d %H:%M')} (Google Calendar)"
                }
            except Exception as cal_err:
                pass

        # Mock response if no calendar credentials
        return {
            **state,
            "calendar_event": {"mock": True, "title": event_data["title"], "start": start.isoformat()},
            "final_response": f"✅ Meeting '{event_data['title']}' scheduled for {start.strftime('%A %d %B %Y at %H:%M')} (1 hour)\n\n_Note: Connect Google Calendar API to save real events._"
        }

    except Exception as e:
        return {**state, "error": str(e), "final_response": f"Could not parse meeting details: {e}"}