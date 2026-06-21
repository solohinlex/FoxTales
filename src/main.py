# src/main.py
import sys
from config import MODEL
from agent import run_agent
from prompts import SYSTEM_PROMPT, Presets
from vector_store import vector_store


def main():
    print("=== FoxTales AI ===\n")

    # ── Индексация при старте ───────────────────────────────
    print("📚 Проверяю индекс...")
    vector_store.index_all()
    print()
    print_help()

    history = []
    current_mode = "search"  # режим по умолчанию

    while True:
        sys.stdout.write(f"[{current_mode}] Ты: ")
        sys.stdout.flush()
        raw = sys.stdin.buffer.readline()
        user_input = raw.decode('utf-8', errors='replace').strip()

        if not user_input:
            continue

        # ── Служебные команды ──────────────────────────────
        if user_input.lower() in ("выход", "exit", "quit"):
            print("Пока!")
            break

        if user_input.lower() == "reindex":
            print("🔄 Принудительная переиндексация...")
            vector_store.index_all(force=True)
            print()
            continue

        if user_input.lower() == "index status":
            vector_store.print_status()
            print()
            continue

        if user_input.lower() == "help":
            print_help()
            continue

        # ── Режимы работы ──────────────────────────────────
        if user_input.lower().startswith("mode "):
            mode = user_input.split(" ", 1)[1].strip()
            if mode in Presets.list_available():
                current_mode = mode
                print(f"✅ Режим установлен: {mode}")
            else:
                print(f"❌ Неизвестный режим. Доступные: {', '.join(Presets.list_available())}")
            print()
            continue

        # ── Основной диалог ────────────────────────────────
        print("Думаю...")
        answer = run_agent(user_input, history, task=current_mode)
        print(f"\nИИ: {answer}\n")


def print_help():
    print("""
📖 Команды:
  reindex       — переиндексировать весь контент заново
  index status  — показать статистику индекса
  mode <name>   — установить режим (search, analysis, editing, lore_check, character, planning)
  help          — эта справка
  выход / exit  — выйти

🎯 Доступные режимы:
  search       — поиск информации
  analysis     — анализ текста
  editing      — редактирование
  lore_check   — проверка на соответствие лору
  character    — работа с персонажами
  planning     — планирование сюжета
    """)


if __name__ == "__main__":
    main()
