# src/config.py

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# ─── Модель ────────────────────────────────────────────────
MODEL = {
    "model": os.getenv("MODEL_NAME", "gpt-4o"),
    "api_key": os.getenv("API_KEY"),
    "api_base": os.getenv("API_BASE") or None,
}

# ─── Пути ──────────────────────────────────────────────────
ROOT         = Path(__file__).parent.parent
CONTENT_PATH = ROOT / "content"
DATA_PATH    = ROOT / "data"
CHROMA_PATH  = DATA_PATH / "chroma_db"

# ─── Структура папок ───────────────────────────────────────
_DIRS = [
    CONTENT_PATH / "works",
    CONTENT_PATH / "characters",
    CONTENT_PATH / "lore",
    CONTENT_PATH / "notes",
    DATA_PATH,
    CHROMA_PATH,
]

for _dir in _DIRS:
    _dir.mkdir(parents=True, exist_ok=True)