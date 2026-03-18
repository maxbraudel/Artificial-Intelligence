import json
import os
from pathlib import Path

MEMORY_DIR = Path(__file__).resolve().parent.parent / "memory"


def _session_path(user_id: int, chat_id: int) -> Path:
    return MEMORY_DIR / f"{user_id}_{chat_id}.json"


def _ensure_dir() -> None:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def load_session(user_id: int, chat_id: int) -> dict:
    path = _session_path(user_id, chat_id)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "user_id": user_id,
        "chat_id": chat_id,
        "cv": None,
        "company": None,
        "interview": {"questions": [], "answers": []},
    }


def save_session(user_id: int, chat_id: int, data: dict) -> None:
    _ensure_dir()
    path = _session_path(user_id, chat_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def reset_session(user_id: int, chat_id: int) -> dict:
    data = {
        "user_id": user_id,
        "chat_id": chat_id,
        "cv": None,
        "company": None,
        "interview": {"questions": [], "answers": []},
    }
    save_session(user_id, chat_id, data)
    return data
