import imaplib
import email
from app.core.config import get_settings

settings = get_settings()

def email_node(state: dict):

    try:
        if not settings.gmail_imap_email:
            return {**state, "final_response": "Email not configured"}

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(settings.gmail_imap_email, settings.gmail_imap_app_password)

        mail.select("INBOX")
        _, data = mail.search(None, "UNSEEN")

        emails = []

        for num in data[0].split()[-5:]:
            _, msg_data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            emails.append(f"{msg.get('subject')} - {msg.get('from')}")

        summary = "\n".join(emails) if emails else "No new emails"

        return {
            **state,
            "final_response": "📧 Emails:\n" + summary
        }

    except Exception as e:
        return {
            **state,
            "final_response": f"Email error: {str(e)}"
        }