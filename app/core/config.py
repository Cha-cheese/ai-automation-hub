from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    google_api_key: str = ""
    gemini_model: str = "gemini-pro"

    tavily_api_key: str = ""
    slack_bot_token: str = ""

    gmail_imap_email: str = ""
    gmail_imap_app_password: str = ""

    upstash_redis_rest_url: str = ""
    upstash_redis_rest_token: str = ""

    demo_mode: bool = False
    request_timeout_seconds: int = 20   # 🔥 reduce from 45 → stable
    llm_timeout_seconds: int = 10
    tavily_timeout_seconds: int = 10

    app_env: str = "production"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()