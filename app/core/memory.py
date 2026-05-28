import json

MEMORY = {}


def save_memory(user_id: str, data: dict):
    MEMORY[user_id] = data


def get_memory(user_id: str):
    return MEMORY.get(user_id, {})