# src/skills/chapters.py
import os
from .base import Skill, SkillResult

CONTENT_PATH = "./content"

class ListWorks(Skill):
    name = "list_works"
    description = "Получить список всех произведений"
    parameters = {"type": "object", "properties": {}}

    def execute(self, **kwargs) -> SkillResult:
        works_path = os.path.join(CONTENT_PATH, "works")
        works = os.listdir(works_path)
        return SkillResult(True, "\n".join(works))


class ListChapters(Skill):
    name = "list_chapters"
    description = "Получить список глав произведения"
    parameters = {
        "type": "object",
        "properties": {
            "work": {
                "type": "string",
                "description": "Название произведения: fox_tales или witch_hounting"
            }
        },
        "required": ["work"]
    }

    def execute(self, work: str, **kwargs) -> SkillResult:
        path = os.path.join(CONTENT_PATH, "works", work, "chapters")
        if not os.path.exists(path):
            return SkillResult(False, f"Произведение не найдено: {work}")
        chapters = sorted(os.listdir(path))
        return SkillResult(True, "\n".join(chapters))


class ReadChapter(Skill):
    name = "read_chapter"
    description = "Прочитать главу произведения"
    parameters = {
        "type": "object",
        "properties": {
            "work": {
                "type": "string",
                "description": "Название произведения: fox_tales или witch_hounting"
            },
            "chapter": {
                "type": "string",
                "description": "Имя файла главы, например: chapter_01.md"
            }
        },
        "required": ["work", "chapter"]
    }

    def execute(self, work: str, chapter: str, **kwargs) -> SkillResult:
        path = os.path.join(CONTENT_PATH, "works", work, "chapters", chapter)
        if not os.path.exists(path):
            return SkillResult(False, f"Глава не найдена: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return SkillResult(True, f.read())


class ReadWorkNotes(Skill):
    name = "read_work_notes"
    description = "Прочитать заметки по конкретному произведению"
    parameters = {
        "type": "object",
        "properties": {
            "work": {"type": "string"}
        },
        "required": ["work"]
    }

    def execute(self, work: str, **kwargs) -> SkillResult:
        path = os.path.join(CONTENT_PATH, "works", work, "notes")
        if not os.path.exists(path):
            return SkillResult(False, f"Заметки не найдены")
        result = ""
        for f in sorted(os.listdir(path)):
            if f.endswith('.md'):
                with open(os.path.join(path, f), 'r', encoding='utf-8') as fp:
                    result += f"\n## {f}\n{fp.read()}\n"
        return SkillResult(True, result)