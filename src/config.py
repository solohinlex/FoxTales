# src/config.py
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# ─── Основная модель ───────────────────────────────────────
_model_name = os.getenv("MODEL_NAME", "gpt-4o")
_api_base   = os.getenv("API_BASE") or None

if _api_base and not _model_name.startswith("openai/"):
    _model_name = f"openai/{_model_name}"

MODEL = {
    "model":    _model_name,
    "api_key":  os.getenv("API_KEY"),
    "api_base": _api_base,
}

# ─── Embedding модель ──────────────────────────────────────
EMBED = {
    # ollama | openai
    "provider": os.getenv("EMBED_PROVIDER", "ollama"),
    "model":    os.getenv("EMBED_MODEL", "nomic-embed-text"),
    # для ollama / локальных серверов
    "base_url": os.getenv("EMBED_BASE_URL", "http://localhost:11434"),
    # для openai — тот же API_KEY
    "api_key":  os.getenv("EMBED_API_KEY") or os.getenv("API_KEY"),
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
