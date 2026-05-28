import imaplib
import email
from app.core.config import get_settings

settings = get_settings()

def email_node(state: dict):
    return {
        **state,
        "final_response": "📧 Email module disabled in production (enable async worker later)"
    }