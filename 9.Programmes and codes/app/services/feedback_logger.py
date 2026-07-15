"""
Feedback Logger Service
--------------------------
Follows the same architectural pattern as the history logger, but captures
explicit user feedback on individual conversation suggestions. This data
forms the foundation for a future recommendation-improvement loop.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
FEEDBACK_FILE = DATA_DIR / "feedback.json"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def log_feedback(suggestion: str, action: str) -> None:
    """
    Append a feedback entry capturing the exact suggestion text, the action
    taken ('like' or 'dislike'), and a timestamp.
    """
    _ensure_data_dir()

    entry = {
        "suggestion": suggestion,
        "action": action,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    feedback = load_feedback()
    feedback.append(entry)

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedback, f, indent=2)


def load_feedback() -> List[Dict[str, Any]]:
    """Return all feedback entries as a list. Always returns a list, even when empty."""
    if not FEEDBACK_FILE.exists():
        return []

    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []
