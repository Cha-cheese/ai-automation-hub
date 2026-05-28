from datetime import datetime, timedelta
import jwt
import os

SECRET = os.getenv("JWT_SECRET", "dev-secret")


def create_token(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=7)
    }

    return jwt.encode(payload, SECRET, algorithm="HS256")