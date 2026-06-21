# src/main.py
from config import MODEL
from agent import run_agent
from prompts import SYSTEM_PROMPT
from vector_store import vector_store


def main():
    print("=== FoxTales AI ===\n")

    # ── Индексация при старте ───────────────────────────────
    print("📚 Проверяю индекс...")
    vector_store.index_all()
    print()
    print_help()

    history = []

    while True:
        user_input = input("Ты: ").strip()

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

        # ── Основной диалог ────────────────────────────────
        print("Думаю...")
        answer = run_agent(user_input, history, SYSTEM_PROMPT)
        print(f"\nИИ: {answer}\n")


def print_help():
    print("""
📖 Команды:
  reindex       — переиндексировать весь контент заново
  index status  — показать статистику индекса
  help          — эта справка
  выход / exit  — выйти
    """)


if __name__ == "__main__":
    main()