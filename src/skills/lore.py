# src/skills/lore.py
import os
from .base import Skill, SkillResult

CONTENT_PATH = "./content"


class ListLore(Skill):
    name = "list_lore"
    description = "Получить список всех доступных файлов лора"
    parameters = {"type": "object", "properties": {}}

    def execute(self, **kwargs) -> SkillResult:
        path = os.path.join(CONTENT_PATH, "lore")
        if not os.path.exists(path):
            return SkillResult(False, "Папка лора не найдена")
        files = [f.replace('.md', '') for f in sorted(os.listdir(path)) if f.endswith('.md')]
        if not files:
            return SkillResult(False, "Файлы лора не найдены")
        return SkillResult(True, "\n".join(files))


class ReadLore(Skill):
    name = "read_lore"
    description = "Прочитать файл лора по названию. Сначала используй list_lore чтобы узнать доступные файлы."
    parameters = {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "Название файла лора без расширения, например: imperia, northlands"
            }
        },
        "required": ["topic"]
    }

    def execute(self, topic: str, **kwargs) -> SkillResult:
        path = os.path.join(CONTENT_PATH, "lore", f"{topic}.md")
        if not os.path.exists(path):
            lore_path = os.path.join(CONTENT_PATH, "lore")
            available = [f.replace('.md', '') for f in os.listdir(lore_path) if f.endswith('.md')]
            return SkillResult(False, f"Лор не найден: '{topic}'. Доступные: {', '.join(available)}")
        with open(path, 'r', encoding='utf-8') as f:
            return SkillResult(True, f.read())


class ListNotes(Skill):
    name = "list_notes"
    description = "Получить список всех доступных общих заметок проекта"
    parameters = {"type": "object", "properties": {}}

    def execute(self, **kwargs) -> SkillResult:
        path = os.path.join(CONTENT_PATH, "notes")
        if not os.path.exists(path):
            return SkillResult(False, "Папка заметок не найдена")
        files = [f.replace('.md', '') for f in sorted(os.listdir(path)) if f.endswith('.md')]
        if not files:
            return SkillResult(False, "Заметки не найдены")
        return SkillResult(True, "\n".join(files))


class ReadNote(Skill):
    name = "read_note"
    description = "Прочитать общую заметку проекта. Сначала используй list_notes чтобы узнать доступные файлы."
    parameters = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Название файла заметки без расширения, например: concepts"
            }
        },
        "required": ["name"]
    }

    def execute(self, name: str, **kwargs) -> SkillResult:
        path = os.path.join(CONTENT_PATH, "notes", f"{name}.md")
        if not os.path.exists(path):
            notes_path = os.path.join(CONTENT_PATH, "notes")
            available = [f.replace('.md', '') for f in os.listdir(notes_path) if f.endswith('.md')]
            return SkillResult(False, f"Заметка не найдена: '{name}'. Доступные: {', '.join(available)}")
        with open(path, 'r', encoding='utf-8') as f:
            return SkillResult(True, f.read())
