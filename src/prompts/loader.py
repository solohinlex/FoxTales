# src/prompts/loader.py
"""Модуль загрузки и управления промптами"""

from pathlib import Path
from typing import Optional
from functools import lru_cache

PROMPTS_DIR = Path(__file__).parent


@lru_cache(maxsize=32)
def load_prompt(name: str) -> str:
    """Загружает промпт из .md файла с кэшированием
    
    Args:
        name: Название промпта (без расширения .md)
    
    Returns:
        Текст промпта
    """
    # Добавляем расширение если нет
    if not name.endswith('.md'):
        name = name + '.md'
    
    path = PROMPTS_DIR / name
    return path.read_text(encoding="utf-8")


# Маппинг вариантов промптов
VARIANT_MAP = {
    "analysis": {
        "default": "analysis",
        "extract": "extract_analysis",
    },
    "character": {
        "default": "character",
        "extract": "extract_character",
    },
}


class PromptBuilder:
    """Конструктор промптов для гибкой композиции"""
    
    def __init__(self):
        self._parts: list[str] = []
    
    def add(self, name: str) -> 'PromptBuilder':
        """Добавить промпт к конструктору
        
        Args:
            name: Название промпта для добавления
        
        Returns:
            self для цепочки вызовов
        """
        self._parts.append(load_prompt(name))
        return self
    
    def add_text(self, text: str) -> 'PromptBuilder':
        """Добавить произвольный текст
        
        Args:
            text: Текст для добавления
        
        Returns:
            self для цепочки вызовов
        """
        self._parts.append(text)
        return self
    
    def build(self) -> str:
        """Собрать финальный промпт
        
        Returns:
            Объединённый текст промпта
        """
        return "\n\n".join(self._parts)


# Фабрика готовых пресетов промптов
class Presets:
    """Наборы промптов для типовых задач"""
    
    @staticmethod
    def for_task(task_name: str, variant: str = "default") -> str:
        """Получить промпт для задачи с поддержкой вариантов
        
        Args:
            task_name: Название задачи
            variant: Вариант промпта ("default" или "extract")
        
        Returns:
            Промпт для задачи
        """
        # Определяем базовый промпт в зависимости от варианта
        system_prompt = "extract" if variant == "extract" else "system"
        
        # Определяем специфичный промпт задачи
        if task_name in VARIANT_MAP:
            task_prompt = VARIANT_MAP[task_name].get(variant, task_name)
        else:
            task_prompt = task_name
        
        builder = PromptBuilder()
        builder.add(system_prompt)
        builder.add(task_prompt)
        return builder.build()
    
    @staticmethod
    def list_available() -> list[str]:
        """Получить список доступных пресетов
        
        Returns:
            Список названий пресетов
        """
        return [
            "analysis",
            "editing",
            "lore_check",
            "character",
            "planning",
            "search",
        ]


# Обратная совместимость — загрузка system промпта
def get_system_prompt() -> str:
    """Получить системный промпт (для обратной совместимости)"""
    return load_prompt("system")