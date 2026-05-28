import uuid

USERS = {
    "admin": "admin123"
}

TOKENS = {}


def login(username, password):
    if USERS.get(username) == password:
        token = str(uuid.uuid4())
        TOKENS[token] = username
        return token
    return None


def verify(token):
    return TOKENS.get(token)