import uuid

TOKENS = {}


def login(username, password):
    if username == "admin" and password == "admin123":
        token = str(uuid.uuid4())
        TOKENS[token] = "admin"
        return token
    return None


def verify_token(token):
    return TOKENS.get(token)