from googleapiclient.discovery import build
from google.oauth2 import service_account
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import get_settings
from datetime import datetime, timedelta
import json

settings = get_settings()
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=settings.anthropic_api_key,
    max_tokens=256,
)

EXTRACT_PROMPT = f"""Extract meeting details from this text. 
Current datetime: {datetime.now().isoformat()}
Return JSON: {{"title": "", "start_time": "ISO8601", "duration_minutes": 60, "description": ""}}
Only JSON, no markdown."""

def calendar_node(state: dict) -> dict:
    try:
        # Extract event details using Claude
        response = llm.invoke([
            SystemMessage(content=EXTRACT_PROMPT),
            HumanMessage(content=state["user_input"])
        ])
        event_data = json.loads(response.content)
        
        start = datetime.fromisoformat(event_data["start_time"])
        end = start + timedelta(minutes=event_data.get("duration_minutes", 60))
        
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
            "final_response": f"Meeting '{event['summary']}' scheduled for {start.strftime('%Y-%m-%d %H:%M')}"
        }
    except Exception as e:
        return {**state, "error": str(e), "final_response": f"Could not schedule: {e}"}