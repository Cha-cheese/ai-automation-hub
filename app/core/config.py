from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    google_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"  # FIX: stable model
    tavily_api_key: str = ""

    gmail_imap_email: str = ""
    gmail_imap_app_password: str = ""

    slack_bot_token: str = ""
    slack_default_channel: str = "#general"

    upstash_redis_rest_url: str = ""
    upstash_redis_rest_token: str = ""

    request_timeout_seconds: int = 25  # FIX: reduce for Render
    demo_mode: bool = False
    app_env: str = "production"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()