import json
from pathlib import Path


def load_service_account_info(raw_value: str) -> dict:
    if not raw_value or raw_value == "{}":
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON is not configured.")

    value = raw_value.strip()
    if value.startswith("{"):
        return json.loads(value)

    path = Path(value).expanduser()
    if not path.exists():
        raise RuntimeError(f"Google service account file not found: {value}")

    return json.loads(path.read_text())
