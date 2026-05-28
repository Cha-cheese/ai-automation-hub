from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    google_api_key: str
    tavily_api_key: str = ""
    google_service_account_json: str = "{}"
    slack_bot_token: str = ""
    slack_default_channel: str = "#general"
    upstash_redis_rest_url: str = ""
    upstash_redis_rest_token: str = ""
    app_env: str = "production"
    secret_key: str = "change-me"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()