# src/web.py
import gradio as gr
import webbrowser
import threading
from agent import run_agent
from prompts import SYSTEM_PROMPT, Presets, PromptBuilder
from vector_store import vector_store
from config import WEB_PORT

# Индексация при старте
vector_store.index_all()

def chat(message, history):
    """Обработчик чата"""
    # history у gradio уже в нужном формате [[user, bot], ...]
    agent_history = []
    for user_msg, bot_msg in history:
        agent_history.append({"role": "user", "content": user_msg})
        agent_history.append({"role": "assistant", "content": bot_msg})
    
    answer = run_agent(message, agent_history, SYSTEM_PROMPT)
    return answer

def reindex():
    """Принудительная переиндексация"""
    vector_store.index_all(force=True)
    return "✅ Переиндексация завершена!"

def get_index_status():
    """Получить статус индекса"""
    total = vector_store._collection.count()
    if total == 0:
        return "📭 Индекс пуст"
    
    all_docs = vector_store._collection.get(include=["metadatas"])
    
    counts = {}
    for meta in all_docs["metadatas"]:
        t = meta.get("type", "unknown")
        counts[t] = counts.get(t, 0) + 1
    
    result = f"📊 Всего документов: {total}\n\n"
    for type_name, count in sorted(counts.items()):
        emoji = {
            "character": "👤",
            "lore":      "🌍",
            "chapter":   "📖",
        }.get(type_name, "📄")
        result += f"  {emoji} {type_name}: {count}\n"
    
    return result

# Создаём интерфейс с вкладками
with gr.Blocks(title="🦊 FoxTales AI") as demo:
    gr.Markdown("# 🦊 FoxTales AI")
    gr.Markdown("Ассистент по миру FoxTales")
    
    with gr.Tabs():
        # Вкладка чата
        with gr.TabItem("💬 Чат"):
            chat_interface = gr.ChatInterface(
                fn=chat,
                title="Диалог с ИИ",
                description="Задавайте вопросы о мире FoxTales",
            )
        
        # Вкладка управления индексом
        with gr.TabItem("📚 Управление индексом"):
            gr.Markdown("### Управление индексом знаний")
            
            status_btn = gr.Button("📊 Обновить статус", variant="secondary")
            status_output = gr.Textbox(label="Статус индекса", lines=10, interactive=False)
            status_btn.click(fn=get_index_status, outputs=status_output)
            
            gr.Markdown("---")
            
            reindex_btn = gr.Button("🔄 Переиндексировать", variant="primary")
            reindex_output = gr.Textbox(label="Результат", interactive=False)
            reindex_btn.click(fn=reindex, outputs=reindex_output)
        
        # Вкладка режимов работы
        with gr.TabItem("🎯 Режимы работы"):
            gr.Markdown("### Выбор режима работы ИИ")
            
            mode_selector = gr.Dropdown(
                label="Режим",
                choices=[
                    ("🔍 Поиск информации", "search"),
                    ("📝 Анализ текста", "analysis"),
                    ("✏️ Редактирование", "editing"),
                    ("🌍 Проверка лора", "lore_check"),
                    ("👤 Персонаж", "character"),
                    ("📋 Планирование", "planning"),
                ],
                value="search"
            )
            
            mode_input = gr.Textbox(
                label="Запрос / Текст",
                placeholder="Введите запрос или текст для анализа...",
                lines=5
            )
            
            mode_output = gr.Textbox(label="Результат", lines=10, interactive=False)
            
            mode_btn = gr.Button("Выполнить", variant="primary")
            
            def run_mode(mode: str, text: str):
                """Запуск агента в выбранном режиме"""
                answer = run_agent(text, [], task=mode)
                return answer
            
            mode_btn.click(
                fn=run_mode,
                inputs=[mode_selector, mode_input],
                outputs=mode_output
            )

def open_browser(url: str):
    """Открыть браузер после небольшой задержки"""
    def _open():
        import time
        time.sleep(1.5)  # Ждём запуска сервера
        webbrowser.open(url)
    threading.Thread(target=_open).start()

if __name__ == "__main__":
    url = f"http://localhost:{WEB_PORT}"
    print(f"\n🌐 Открываю браузер... Если не открылся, перейдите по ссылке: {url}\n")
    
    # Открываем браузер вручную
    open_browser(url)
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=WEB_PORT,
        inbrowser=False  # Используем свой метод
    )
