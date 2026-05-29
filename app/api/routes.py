from fastapi import FastAPI, Header, Request
from pydantic import BaseModel

from app.agents.orchestrator import automation_graph
from app.core.auth import login as auth_login, verify_token

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import os


# =========================
# APP
# =========================

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="CHANGE_THIS_SECRET_KEY",
    same_site="lax"
)


# =========================
# OAUTH
# =========================

config = Config(environ=os.environ)

oauth = OAuth(config)

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile https://www.googleapis.com/auth/gmail.readonly"
    }
)


# =========================
# FRONTEND
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

print("FRONTEND_DIR:", FRONTEND_DIR)
print("EXISTS:", os.path.exists(FRONTEND_DIR))

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


# =========================
# MODELS
# =========================

class LoginReq(BaseModel):
    username: str
    password: str


class AutomateReq(BaseModel):
    message: str


# =========================
# ROUTES
# =========================

@app.get("/")
def root():

    return FileResponse(
        os.path.join(FRONTEND_DIR, "index.html")
    )


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post("/login")
def login_api(req: LoginReq):

    token = auth_login(
        req.username,
        req.password
    )

    if not token:
        return {
            "error": "invalid credentials"
        }

    return {
        "token": token
    }


@app.post("/automate")
def automate(
    req: AutomateReq,
    authorization: str = Header(None)
):

    user = verify_token(authorization)

    if not user:
        return {
            "error": "unauthorized"
        }

    result = automation_graph({
        "user_input": req.message
    })

    return {
        "result": result.get("result"),
        "intent": result.get("intent")
    }


# =========================
# GOOGLE LOGIN
# =========================

@app.get("/auth/login")
async def login_google(request: Request):

    redirect_uri = "https://ai-automation-hub-42r9.onrender.com/auth/callback"

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        prompt="select_account"
    )


@app.get("/auth/callback")
async def auth_callback(request: Request):

    try:

        token = await oauth.google.authorize_access_token(request)

        user = token.get("userinfo")

        request.session["access_token"] = token["access_token"]
        request.session["user_email"] = user["email"]

        return RedirectResponse(url="/")

    except Exception as e:

        return {
            "error": str(e)
        }


# =========================
# GMAIL UNREAD
# =========================

@app.get("/gmail/unread")
async def get_unread_emails(request: Request):

    access_token = request.session.get("access_token")

    if not access_token:
        return {
            "error": "not logged in"
        }

    credentials = Credentials(
        token=access_token
    )

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    results = service.users().messages().list(
        userId="me",
        labelIds=["UNREAD"],
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for msg in messages:

        message = service.users().messages().get(
            userId="me",
            id=msg["id"]
        ).execute()

        headers = message["payload"]["headers"]

        subject = "(No Subject)"

        for h in headers:

            if h["name"] == "Subject":
                subject = h["value"]

        emails.append({
            "id": msg["id"],
            "subject": subject
        })

    return {
        "emails": emails
    }