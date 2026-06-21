# src/vector_store.py
import yaml
import chromadb
from config import CONTENT_PATH, CHROMA_PATH, EMBED
from embeddings import get_embedding
from chromadb.api.models.Collection import Collection
from chromadb.api.types import EmbeddingFunction

# ── Константы чанкинга ─────────────────────────────────
CHUNK_SIZE = 1500      # символов в чанке
CHUNK_OVERLAP = 300    # перекрытие между чанками

def _split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Разбить текст на чанки с перекрытием"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # Если не последний чанк — обрезаем по последнему переносу строки
        if end < len(text):
            last_newline = chunk.rfind("\n")
            if last_newline > chunk_size // 2:
                chunk = chunk[:last_newline]

        chunks.append(chunk.strip())

        # ← ФИКС: шаг всегда вперёд, минимум 1 символ
        step = len(chunk) - overlap
        if step < 1:
            step = chunk_size - overlap  # fallback на полный шаг
        start += step

    return [c for c in chunks if c]
    
def _load_all_documents() -> list[dict]:
    """Загрузить все документы из content/"""
    docs = []

    # ── Персонажи ──────────────────────────────────────────
    chars_path = CONTENT_PATH / "characters"
    for yml_file in chars_path.glob("*.yml"):
        if yml_file.name == ".gitkeep":
            continue
        with open(yml_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not data:
            continue

        # Собираем текст из всех полей
        parts = []
        for key, val in data.items():
            if val:
                parts.append(f"{key}: {val}")
        text = "\n".join(parts)

        docs.append({
            "id": f"character::{yml_file.stem}",
            "text": text,
            "metadata": {
                "type": "character",
                "name": yml_file.stem,
                "source": str(yml_file.relative_to(CONTENT_PATH))
            }
        })

    # ── Lore ───────────────────────────────────────────────
    lore_path = CONTENT_PATH / "lore"
    for md_file in lore_path.glob("*.md"):
        text = md_file.read_text(encoding="utf-8").strip()
        if not text:
            continue
        docs.append({
            "id": f"lore::{md_file.stem}",
            "text": text,
            "metadata": {
                "type": "lore",
                "name": md_file.stem,
                "source": str(md_file.relative_to(CONTENT_PATH))
            }
        })

    # ── Главы произведений ────────────────────────────────
    works_path = CONTENT_PATH / "works"
    for chapter_file in works_path.rglob("chapters/*.md"):
        text = chapter_file.read_text(encoding="utf-8").strip()
        if not text:
            continue

        work_name = chapter_file.parts[-3]
        chunks = _split_text(text)

        for i, chunk in enumerate(chunks):
            docs.append({
                "id": f"chapter::{work_name}::{chapter_file.stem}::chunk_{i}",
                "text": chunk,
                "metadata": {
                    "type": "chapter",
                    "work": work_name,
                    "chapter": chapter_file.stem,
                    "chunk_index": i,
                    "chunks_total": len(chunks),
                    "source": str(chapter_file.relative_to(CONTENT_PATH))
                }
            })
            
    return docs


class VectorStore:
    """Обёртка над ChromaDB"""

    def __init__(self):
        self._client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        self._collection = self._client.get_or_create_collection(
            name="foxtales",
            metadata={"hnsw:space": "cosine"},
            embedding_function=None   # отключаем дефолтную модель chromadb
        )

    def index_all(self, force: bool = False):
        """Проиндексировать весь контент"""
        docs = _load_all_documents()

        # Проверяем что уже есть в базе
        existing_ids = set(self._collection.get()["ids"])

        to_add = []
        for doc in docs:
            if force or doc["id"] not in existing_ids:
                to_add.append(doc)

        if not to_add:
            print(f"  ✅ ChromaDB актуальна ({len(existing_ids)} документов)")
            return

        print(f"  📥 Индексирую {len(to_add)} документов...")

        for doc in to_add:
            embedding = get_embedding(doc["text"])
            self._collection.upsert(
                ids=[doc["id"]],
                embeddings=[embedding],
                documents=[doc["text"]],
                metadatas=[doc["metadata"]]
            )
            print(f"     ✓ {doc['id']}")

        print(f"  ✅ Готово! Всего в базе: {self._collection.count()}")

    def search(self, query: str, n_results: int = 5, where: dict = None) -> list[dict]:
        """Семантический поиск"""
        total = self._collection.count()
        if total == 0:
            return []
        query_embedding = get_embedding(query)

        kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": min(n_results, self._collection.count()),
            "include": ["documents", "metadatas", "distances"]
        }
        if where:
            kwargs["where"] = where

        results = self._collection.query(**kwargs)

        output = []
        for i in range(len(results["ids"][0])):
            output.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "score": 1 - results["distances"][0][i]  # cosine → similarity
            })

        return output

    def print_status(self):
        """Показать статистику индекса"""
        # Показываем текущий провайдер
        print(f"  🤖 Embedding: {EMBED['provider']} / {EMBED['model']}")

        total = self._collection.count()
        if total == 0:
            print("  📭 Индекс пуст")
            return

        all_docs = self._collection.get(include=["metadatas"])

        counts = {}
        for meta in all_docs["metadatas"]:
            t = meta.get("type", "unknown")
            counts[t] = counts.get(t, 0) + 1

        print(f"  📊 Всего документов: {total}")
        for type_name, count in sorted(counts.items()):
            emoji = {
                "character": "👤",
                "lore":      "🌍",
                "chapter":   "📖",
            }.get(type_name, "📄")
            print(f"     {emoji} {type_name}: {count}")
            
# Синглтон — создаётся один раз при импорте
vector_store = VectorStore()
