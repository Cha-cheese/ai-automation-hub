import jwt
import datetime
import os

SECRET = os.getenv("JWT_SECRET", "secret")


def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def verify_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        return None