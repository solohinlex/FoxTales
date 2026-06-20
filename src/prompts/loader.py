# src/prompts/loader.py

from pathlib import Path

PROMPTS_DIR = Path(__file__).parent


def load_prompt(filename: str) -> str:
    """Загружает промпт из .md файла"""
    path = PROMPTS_DIR / filename
    return path.read_text(encoding="utf-8")