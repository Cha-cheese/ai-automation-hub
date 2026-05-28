from googleapiclient.discovery import build
from google.oauth2 import service_account
from app.core.config import get_settings
from app.core.errors import safe_error_message
from app.tools.google_tools import load_service_account_info
import email
import imaplib

settings = get_settings()

def get_unread_emails_from_imap() -> list:
    if not settings.gmail_imap_email or not settings.gmail_imap_app_password:
        raise RuntimeError("GMAIL_IMAP_EMAIL and GMAIL_IMAP_APP_PASSWORD are not configured.")

    with imaplib.IMAP4_SSL("imap.gmail.com", 993) as mail:
        mail.login(settings.gmail_imap_email, settings.gmail_imap_app_password)
        mail.select("INBOX")
        status, data = mail.search(None, "UNSEEN")
        if status != "OK":
            raise RuntimeError("Could not search unread Gmail messages via IMAP.")

        message_ids = data[0].split()[-5:]
        emails = []
        for message_id in reversed(message_ids):
            status, msg_data = mail.fetch(message_id, "(RFC822)")
            if status != "OK" or not msg_data:
                continue

            raw_message = msg_data[0][1]
            parsed = email.message_from_bytes(raw_message)
            body = ""
            if parsed.is_multipart():
                for part in parsed.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
                            break
            else:
                payload = parsed.get_payload(decode=True)
                if payload:
                    body = payload.decode(parsed.get_content_charset() or "utf-8", errors="replace")

            emails.append({
                "id": message_id.decode(),
                "from": parsed.get("From", ""),
                "subject": parsed.get("Subject", ""),
                "snippet": " ".join(body.split())[:300],
            })

        return emails

def get_gmail_service():
    creds_json = load_service_account_info(settings.google_service_account_json)
    creds = service_account.Credentials.from_service_account_info(
        creds_json,
        scopes=["https://www.googleapis.com/auth/gmail.readonly"]
    )
    return build("gmail", "v1", credentials=creds)

def email_node(state: dict) -> dict:
    try:
        if settings.gmail_imap_email and settings.gmail_imap_app_password:
            emails = get_unread_emails_from_imap()
            return {**state, "email_data": {"emails": emails, "count": len(emails)}}

        if settings.google_service_account_json in ("", "{}"):
            raise RuntimeError(
                "Gmail is not configured. For a personal Gmail account, set "
                "GMAIL_IMAP_EMAIL and GMAIL_IMAP_APP_PASSWORD in Render."
            )

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
        message = safe_error_message(e)
        if "failedPrecondition" in message or "Precondition check failed" in message:
            message = (
                "Gmail service account access failed. For a personal Gmail account, set "
                "GMAIL_IMAP_EMAIL and GMAIL_IMAP_APP_PASSWORD in Render instead. "
                "Service accounts only work for Gmail with Google Workspace domain-wide delegation."
            )
        return {**state, "email_data": {}, "error": message}
