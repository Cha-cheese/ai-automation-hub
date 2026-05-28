import re


def safe_error_message(error: object) -> str:
    message = str(error)
    message = re.sub(r"([?&]key=)[^'\"\s&]+", r"\1[redacted]", message)
    message = re.sub(r"(api[_-]?key['\"]?\s*[:=]\s*['\"]?)[^'\"\s,}]+", r"\1[redacted]", message, flags=re.IGNORECASE)
    return message

def safe_error_message(e: Exception) -> str:
    return str(e).split("\n")[0]