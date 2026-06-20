# src/skills/search.py
import os
from .base import Skill, SkillResult

CONTENT_PATH = "./content"

class SearchContent(Skill):
    name = "search_content"
    description = "Поиск по всему контенту проекта"
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Поисковый запрос"
            },
            "work": {
                "type": "string",
                "description": "Ограничить поиск произведением (опционально)"
            }
        },
        "required": ["query"]
    }

    def execute(self, query: str, work: str = None, **kwargs) -> SkillResult:
        results = []
        base = os.path.join(CONTENT_PATH, "works", work) if work else CONTENT_PATH

        for root, dirs, files in os.walk(base):
            # Пропускаем папки с изображениями
            dirs[:] = [d for d in dirs if d != 'images']
            for filename in files:
                if not filename.endswith(('.md', '.txt', '.yml')):
                    continue
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    if query.lower() in line.lower():
                        context_start = max(0, i - 1)
                        context_end = min(len(lines), i + 2)
                        context = "".join(lines[context_start:context_end]).strip()
                        rel_path = os.path.relpath(filepath, CONTENT_PATH)
                        results.append(f"📄 {rel_path}:{i+1}\n{context}")

        if not results:
            return SkillResult(False, f"Ничего не найдено: '{query}'")

        output = f"🔍 '{query}' — {len(results)} совпадений:\n\n"
        output += "\n\n---\n\n".join(results[:10])
        if len(results) > 10:
            output += f"\n\n...и ещё {len(results) - 10}"
        return SkillResult(True, output)