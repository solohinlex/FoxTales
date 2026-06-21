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
    def for_task(task_name: str) -> str:
        """Получить промпт для задачи
        
        Args:
            task_name: Название задачи
        
        Returns:
            Промпт для задачи
        """
        presets = {
            "analysis": lambda: PromptBuilder()
                .add("system")
                .add("analysis")
                .build(),
            
            "editing": lambda: PromptBuilder()
                .add("system")
                .add("editing")
                .build(),
            
            "lore_check": lambda: PromptBuilder()
                .add("system")
                .add("lore_check")
                .build(),
            
            "character": lambda: PromptBuilder()
                .add("system")
                .add("character")
                .build(),
            
            "planning": lambda: PromptBuilder()
                .add("system")
                .add("planning")
                .build(),
            
            "search": lambda: PromptBuilder()
                .add("system")
                .add("search")
                .build(),
        }
        
        if task_name not in presets:
            return load_prompt("system")
        
        return presets[task_name]()
    
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