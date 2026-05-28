from app.core.config import get_settings
from app.core.errors import safe_error_message
from app.agents.demo_data import DEMO_EMAILS

import email
import imaplib

from email.header import decode_header


settings = get_settings()


def decode_mime_words(s):
    if not s:
        return ""

    decoded = decode_header(s)
    result = ""

    for part, encoding in decoded:
        if isinstance(part, bytes):
            result += part.decode(encoding or "utf-8", errors="replace")
        else:
            result += part

    return result


def get_unread_emails_from_imap() -> list:
    if not settings.gmail_imap_email or not settings.gmail_imap_app_password:
        raise RuntimeError(
            "GMAIL_IMAP_EMAIL and GMAIL_IMAP_APP_PASSWORD are not configured."
        )

    with imaplib.IMAP4_SSL("imap.gmail.com", 993) as mail:
        mail.login(
            settings.gmail_imap_email,
            settings.gmail_imap_app_password
        )

        mail.select("INBOX")

        status, data = mail.search(None, "UNSEEN")

        if status != "OK":
            raise RuntimeError("Could not fetch unread emails.")

        message_ids = data[0].split()[-5:]

        emails = []

        for message_id in reversed(message_ids):
            status, msg_data = mail.fetch(message_id, "(RFC822)")

            if status != "OK":
                continue

            raw_message = msg_data[0][1]

            parsed = email.message_from_bytes(raw_message)

            subject = decode_mime_words(parsed.get("Subject", ""))

            sender = decode_mime_words(parsed.get("From", ""))

            body = ""

            if parsed.is_multipart():
                for part in parsed.walk():
                    content_type = part.get_content_type()

                    if content_type == "text/plain":
                        payload = part.get_payload(decode=True)

                        if payload:
                            body = payload.decode(
                                part.get_content_charset() or "utf-8",
                                errors="replace"
                            )

                            break
            else:
                payload = parsed.get_payload(decode=True)

                if payload:
                    body = payload.decode(
                        parsed.get_content_charset() or "utf-8",
                        errors="replace"
                    )

            emails.append({
                "id": message_id.decode(),
                "from": sender,
                "subject": subject,
                "snippet": " ".join(body.split())[:300]
            })

        return emails


def email_node(state: dict) -> dict:
    try:
        if settings.demo_mode:
            return {
                **state,
                "email_data": {
                    "emails": DEMO_EMAILS,
                    "count": len(DEMO_EMAILS),
                }
            }

        emails = get_unread_emails_from_imap()

        return {
            **state,
            "email_data": {
                "emails": emails,
                "count": len(emails),
            }
        }

    except Exception as e:
        return {
            **state,
            "email_data": {},
            "error": safe_error_message(e),
            "final_response": (
                "Could not access Gmail inbox. "
                "Check GMAIL_IMAP_EMAIL and GMAIL_IMAP_APP_PASSWORD."
            )
        }