# src/skills/chapters.py
import os
import yaml
from .base import Skill, SkillResult

CONTENT_PATH = "./content"


def _load_work_meta(work: str) -> dict:
    """Загрузить мета-информацию о произведении"""
    meta_path = os.path.join(CONTENT_PATH, "works", work, "meta.yml")
    if not os.path.exists(meta_path):
        return {}
    with open(meta_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def _get_chapters_list(work: str) -> list:
    """Получить список глав произведения"""
    path = os.path.join(CONTENT_PATH, "works", work, "chapters")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))


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
    description = "Прочитать главу произведения с контекстом всего произведения"
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
        chapter_path = os.path.join(CONTENT_PATH, "works", work, "chapters", chapter)
        if not os.path.exists(chapter_path):
            return SkillResult(False, f"Глава не найдена: {chapter}")
        
        # Читаем главу
        with open(chapter_path, 'r', encoding='utf-8') as f:
            chapter_content = f.read()
        
        # Загружаем мета-информацию о произведении
        work_meta = _load_work_meta(work)
        
        # Формируем контекст произведения
        work_info = []
        work_info.append(f"=== ПРОИЗВЕДЕНИЕ: {work_meta.get('title', work)} ===")
        work_info.append(f"Описание: {work_meta.get('description', 'Описание отсутствует')}")
        work_info.append(f"Статус: {work_meta.get('status', 'unknown')}")
        work_info.append(f"Создано: {work_meta.get('created_at', 'unknown')}")
        work_info.append(f"Обновлено: {work_meta.get('updated_at', 'unknown')}")
        
        # Добавляем информацию о персонажах
        characters = work_meta.get('characters', [])
        if characters:
            work_info.append(f"\nПерсонажи: {', '.join(characters)}")
        
        # Добавляем информацию о главах
        chapters_list = _get_chapters_list(work)
        if chapters_list:
            work_info.append(f"\nВсего глав: {len(chapters_list)}")
            work_info.append("Список глав:")
            for i, ch in enumerate(chapters_list, 1):
                work_info.append(f"  {i}. {ch}")
        
        work_context = "\n".join(work_info)
        
        # Формируем итоговый результат
        result = f"{work_context}\n\n=== ГЛАВА: {chapter} ===\n{chapter_content}"
        
        return SkillResult(True, result)


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
