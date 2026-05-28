from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Gemini
    google_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"

    # Tavily
    tavily_api_key: str = ""

    # Google
    google_service_account_json: str = "{}"

    # Gmail IMAP
    gmail_imap_email: str = ""
    gmail_imap_app_password: str = ""

    # Slack
    slack_bot_token: str = ""
    slack_default_channel: str = "#ai"

    # Redis
    upstash_redis_rest_url: str = ""
    upstash_redis_rest_token: str = ""

    # Timeouts
    request_timeout_seconds: int = 45
    llm_timeout_seconds: int = 20
    tavily_timeout_seconds: int = 12

    # App
    demo_mode: bool = False
    app_env: str = "production"
    secret_key: str = "change-me"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()