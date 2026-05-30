from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar"
]

def get_creds():
    service_account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

    creds = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=SCOPES
    )
    return creds


def get_gmail_service():
    creds = get_creds()
    return build("gmail", "v1", credentials=creds)


def get_calendar_service():
    creds = get_creds()
    return build("calendar", "v3", credentials=creds)