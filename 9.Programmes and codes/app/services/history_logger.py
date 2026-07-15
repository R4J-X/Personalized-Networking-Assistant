"""
History Logger Service
-------------------------
Provides persistent storage for conversation sessions, enabling the
'View Previous Conversations' feature in the frontend and allowing users to
revisit past interactions for reflection and learning.

Uses a simple append-to-JSON-list, read-modify-write pattern, which is
sufficient for single-process, locally-deployed use.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

# pathlib.Path ensures cross-platform compatibility -- the same code works
# correctly on Windows, macOS, and Linux without modification.
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
HISTORY_FILE = DATA_DIR / "history.json"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def log_conversation(entry: Dict[str, Any]) -> None:
    """
    Append a conversation entry to the history file, stamping it with the
    current ISO-formatted UTC timestamp.
    """
    _ensure_data_dir()

    entry_with_timestamp = {**entry, "timestamp": datetime.now(timezone.utc).isoformat()}

    history = load_history()
    history.append(entry_with_timestamp)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def load_history() -> List[Dict[str, Any]]:
    """
    Return the full conversation history as a list.
    Always returns a list, even when no history has been saved yet.
    """
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []
