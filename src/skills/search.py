# src/skills/search.py
from .base import Skill, SkillResult
from vector_store import vector_store


class SearchContent(Skill):
    name = "search_content"
    description = (
        "Семантический поиск по всему контенту проекта: "
        "персонажи, лор, главы произведений. "
        "Понимает смысл, а не только точные совпадения слов."
    )
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Поисковый запрос на естественном языке"
            },
            "type": {
                "type": "string",
                "enum": ["character", "lore", "chapter"],
                "description": "Ограничить поиск типом контента (опционально)"
            },
            "work": {
                "type": "string",
                "description": "Ограничить поиск произведением: fox_tales или witch_hounting (опционально)"
            }
        },
        "required": ["query"]
    }

    def execute(self, query: str, type: str = None, work: str = None, **kwargs) -> SkillResult:
        # Фильтры для ChromaDB
        where = None
        if type and work:
            where = {"$and": [{"type": {"$eq": type}}, {"work": {"$eq": work}}]}
        elif type:
            where = {"type": {"$eq": type}}
        elif work:
            where = {"work": {"$eq": work}}

        results = vector_store.search(query, n_results=5, where=where)

        if not results:
            return SkillResult(False, f"Ничего не найдено по запросу: '{query}'")

        lines = [f"🔍 Результаты поиска: '{query}'\n"]
        for r in results:
            meta = r["metadata"]
            score = r["score"]
            source = meta.get("source", "?")
            lines.append(f"📄 {source} (релевантность: {score:.2f})")
            lines.append(r["text"][:500])  # первые 500 символов
            lines.append("---")

        return SkillResult(True, "\n".join(lines))