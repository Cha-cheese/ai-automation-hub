from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    google_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    tavily_api_key: str = ""
    google_service_account_json: str = "{}"
    slack_bot_token: str = ""
    slack_default_channel: str = "#general"
    upstash_redis_rest_url: str = ""
    upstash_redis_rest_token: str = ""
    request_timeout_seconds: int = 45
    llm_timeout_seconds: int = 20
    tavily_timeout_seconds: int = 12
    app_env: str = "production"
    secret_key: str = "change-me"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
