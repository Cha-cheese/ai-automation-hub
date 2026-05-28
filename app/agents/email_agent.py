import imaplib
import email
from app.core.config import get_settings

settings = get_settings()


def email_node(state: dict):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(settings.gmail_imap_email, settings.gmail_imap_app_password)

        mail.select("INBOX")
        _, data = mail.search(None, "UNSEEN")

        emails = []

        for num in data[0].split()[-5:]:
            _, msg_data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            emails.append({
                "subject": msg.get("subject", "No subject"),
                "from": msg.get("from", "unknown")
            })

        if not emails:
            summary = "No new emails"
        else:
            summary = "\n".join([f"- {e['subject']} | {e['from']}" for e in emails])

        return {
            **state,
            "email_data": emails,
            "final_response": f"📧 EMAIL SUMMARY:\n{summary}",
            "intent": "email"
        }

    except Exception as e:
        return {
            **state,
            "final_response": "Email error",
            "error": str(e)
        }