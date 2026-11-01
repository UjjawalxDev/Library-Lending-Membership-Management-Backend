"""Small JSON persistence helpers. No database or third-party packages needed."""

import json
from pathlib import Path


def save_records(path, items, members, loans):
    data = {
        "items": [
            {
                "type": item.__class__.__name__,
                "item_id": item.item_id,
                "title": item.title,
                "is_available": item.is_available,
            }
            for item in items.values()
        ],
        "members": [
            {
                "type": member.__class__.__name__,
                "member_id": member.member_id,
                "name": member.name,
                "borrowing_limit": member.borrowing_limit,
            }
            for member in members.values()
        ],
        "loans": list(loans.values()),
    }

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_records(path):
    file_path = Path(path)
    if not file_path.exists():
        return {"items": [], "members": [], "loans": []}

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("The saved file must contain a JSON object.")
        return {
            "items": data.get("items", []) if isinstance(data.get("items", []), list) else [],
            "members": data.get("members", []) if isinstance(data.get("members", []), list) else [],
            "loans": data.get("loans", []) if isinstance(data.get("loans", []), list) else [],
        }
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Couldn't read saved library data ({error}). Starting with empty records.")
        return {"items": [], "members": [], "loans": []}
