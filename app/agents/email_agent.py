import imaplib
import email
from app.core.config import get_settings

settings = get_settings()

def email_node(state: dict):

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(settings.gmail_imap_email, settings.gmail_imap_app_password)

        mail.select("inbox")
        _, data = mail.search(None, "UNSEEN")

        emails = []

        for num in data[0].split()[-5:]:
            _, msg_data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            emails.append({
                "from": msg["from"],
                "subject": msg["subject"]
            })

        summary = "\n".join([f"- {e['subject']}" for e in emails])

        return {
            **state,
            "final_response": f"📧 Emails:\n{summary}"
        }

    except Exception as e:
        return {
            **state,
            "final_response": f"Email error: {str(e)}"
        }