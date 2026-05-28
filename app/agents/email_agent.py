from googleapiclient.discovery import build
from google.oauth2 import service_account
from app.core.config import get_settings
from app.core.errors import safe_error_message
from app.tools.google_tools import load_service_account_info

settings = get_settings()

def get_gmail_service():
    creds_json = load_service_account_info(settings.google_service_account_json)
    creds = service_account.Credentials.from_service_account_info(
        creds_json,
        scopes=["https://www.googleapis.com/auth/gmail.readonly"]
    )
    return build("gmail", "v1", credentials=creds)

def email_node(state: dict) -> dict:
    try:
        service = get_gmail_service()
        # Get latest 5 unread emails
        results = service.users().messages().list(
            userId="me", q="is:unread", maxResults=5
        ).execute()
        messages = results.get("messages", [])
        
        emails = []
        for msg in messages:
            detail = service.users().messages().get(
                userId="me", id=msg["id"], format="full"
            ).execute()
            headers = {h["name"]: h["value"] for h in detail["payload"]["headers"]}
            snippet = detail.get("snippet", "")
            emails.append({
                "id": msg["id"],
                "from": headers.get("From", ""),
                "subject": headers.get("Subject", ""),
                "snippet": snippet,
            })
        
        return {**state, "email_data": {"emails": emails, "count": len(emails)}}
    except Exception as e:
        return {**state, "email_data": {}, "error": safe_error_message(e)}
