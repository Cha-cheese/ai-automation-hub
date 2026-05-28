from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import get_settings
from app.core.errors import safe_error_message
from app.agents.llm import build_gemini_llm, clean_json_response
from app.agents.demo_data import demo_calendar_event
from app.tools.google_tools import load_service_account_info
from datetime import datetime, timedelta
import json

settings = get_settings()

EXTRACT_PROMPT = f"""Extract meeting details from this text.
Current datetime: {datetime.now().isoformat()}
Return JSON only (no markdown, no code blocks):
{{"title": "", "start_time": "ISO8601", "duration_minutes": 60, "description": ""}}"""

def calendar_node(state: dict) -> dict:
    try:
        if settings.demo_mode:
            event_data = demo_calendar_event(state["user_input"])
            start = datetime.fromisoformat(event_data["start"])
            return {
                **state,
                "calendar_event": event_data,
                "final_response": (
                    f"✅ Demo meeting scheduled for {start.strftime('%A %d %B %Y at %H:%M')} "
                    "(mock Google Calendar event)."
                ),
            }

        llm = build_gemini_llm(max_tokens=256)
        response = llm.invoke([
            SystemMessage(content=EXTRACT_PROMPT),
            HumanMessage(content=state["user_input"])
        ])
        event_data = json.loads(clean_json_response(response.content))

        start = datetime.fromisoformat(event_data["start_time"])
        end = start + timedelta(minutes=event_data.get("duration_minutes", 60))

        # Try real Google Calendar if credentials exist
        if settings.google_service_account_json not in ("", "{}"):
            try:
                from googleapiclient.discovery import build
                from google.oauth2 import service_account
                creds_json = load_service_account_info(settings.google_service_account_json)
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
                return {
                    **state,
                    "calendar_event": {"mock": True, "title": event_data["title"], "start": start.isoformat()},
                    "error": safe_error_message(cal_err),
                    "final_response": (
                        f"Meeting '{event_data['title']}' parsed for {start.strftime('%A %d %B %Y at %H:%M')}, "
                        "but Google Calendar could not be reached. Showing a mock event instead."
                    )
                }

        # Mock response if no calendar credentials
        return {
            **state,
            "calendar_event": {"mock": True, "title": event_data["title"], "start": start.isoformat()},
            "final_response": f"✅ Meeting '{event_data['title']}' scheduled for {start.strftime('%A %d %B %Y at %H:%M')} (1 hour)\n\n_Note: Connect Google Calendar API to save real events._"
        }

    except Exception as e:
        return {
            **state,
            "error": safe_error_message(e),
            "final_response": (
                "Could not create a calendar event yet. Make sure GOOGLE_API_KEY is set for date parsing, "
                "and GOOGLE_SERVICE_ACCOUNT_JSON is set if you want real Google Calendar writes."
            )
        }
