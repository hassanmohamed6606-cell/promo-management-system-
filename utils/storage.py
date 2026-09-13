import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def load_json(filename):
    path = DATA_DIR / filename
    if not path.exists():
        path.write_text("[]", encoding="utf-8")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

def save_json(filename, data):
    path = DATA_DIR / filename
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
