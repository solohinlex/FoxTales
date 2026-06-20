# src/config.py

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# ─── Модель ────────────────────────────────────────────────
_model_name = os.getenv("MODEL_NAME", "gpt-4o")
_api_base   = os.getenv("API_BASE") or None

# Если задан локальный сервер — litellm требует префикс openai/
if _api_base and not _model_name.startswith("openai/"):
    _model_name = f"openai/{_model_name}"

MODEL = {
    "model":    _model_name,
    "api_key":  os.getenv("API_KEY"),
    "api_base": _api_base,
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