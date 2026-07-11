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

# ─── Авто-определение режима ─────────────────────────────────
MODE_KEYWORDS = {
    "analysis": ["проанализируй", "анализ", "оцени", "разбери", "критика", "сильные стороны", "слабые стороны"],
    "editing": ["отредактируй", "исправь", "улучши", "правки", "редактирование", "стилистика"],
    "lore_check": ["проверь лор", "соответствует канону", "противоречие", "канон", "лор"],
    "character": ["персонаж", "создай персонажа", "придумай персонажа", "карточка персонажа"],
    "planning": ["план", "планирован", "структура", "сюжет", "распиши план", "оглавление"],
    "search": ["найди", "поиск", "что известно", "где упоминается", "информация"],
}

def detect_mode(message: str) -> str:
    """Определить режим на основе ключевых слов в запросе"""
    message_lower = message.lower()
    
    for mode, keywords in MODE_KEYWORDS.items():
        if any(keyword in message_lower for keyword in keywords):
            return mode
    
    return "search"  # режим по умолчанию


# ── Обработчики ─────────────────────────────────────────────
def chat(message, history, mode_selector):
    """Обработчик чата с авто-определением или ручным выбором режима"""
    # Определяем режим: если выбран "auto" — определяем автоматически
    if mode_selector == "auto":
        detected_mode = detect_mode(message)
    else:
        detected_mode = mode_selector
    
    agent_history = []
    for user_msg, bot_msg in history:
        agent_history.append({"role": "user", "content": user_msg})
        agent_history.append({"role": "assistant", "content": bot_msg})
    
    answer = run_agent(message, agent_history, SYSTEM_PROMPT, task=detected_mode)
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

# ── Интерфейс ───────────────────────────────────────────────
CUSTOM_CSS = """
.chat-container {
    height: calc(100vh - 200px) !important;
}
.chatbot-container {
    height: calc(100vh - 200px) !important;
}
.right-panel {
    height: 100% !important;
}
.right-panel .gr-box {
    height: auto !important;
}
.right-panel .gr-button {
    height: auto !important;
    min-height: 40px;
}
.right-panel textarea {
    min-height: 200px !important;
    flex-grow: 1 !important;
}
"""

with gr.Blocks(title="🦊 FoxTales AI", css=CUSTOM_CSS) as demo:
    gr.Markdown("# 🦊 FoxTales AI")
    gr.Markdown("Ассистент по миру FoxTales")
    
    with gr.Tabs():
        # Вкладка чата
        with gr.TabItem("💬 Чат"):
            with gr.Row(equal_height=True):
                # Левая колонка - чатбот
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(
                        label="Диалог с ИИ",
                        height=600,
                        container=False,
                        elem_classes=["chatbot-container"]
                    )
                
                # Правая колонка - управление
                with gr.Column(scale=1, elem_classes=["right-panel"]):
                    mode_selector = gr.Dropdown(
                        choices=[
                            ("🤖 Авто-определение", "auto"),
                            ("🔍 Поиск информации", "search"),
                            ("📝 Анализ текста", "analysis"),
                            ("✏️ Редактирование", "editing"),
                            ("🌍 Проверка лора", "lore_check"),
                            ("👤 Персонаж", "character"),
                            ("📋 Планирование", "planning"),
                        ],
                        value="auto",
                        label="Режим"
                    )
                    msg_input = gr.Textbox(
                        label="Сообщение",
                        placeholder="Задайте вопрос о мире FoxTales...",
                        lines=5
                    )
                    send_btn = gr.Button("Отправить", variant="primary")
            
            def add_user_message(message, history):
                """Добавляет сообщение пользователя в историю"""
                history = history or []
                history.append({"role": "user", "content": message})
                return "", history
            
            def bot_response(history, mode):
                """Генерирует ответ бота"""
                if not history or history[-1].get("role") != "user":
                    return history
                
                # message может быть строкой или списком (в зависимости от версии Gradio)
                message_content = history[-1]["content"]
                if isinstance(message_content, list):
                    message = message_content[0].get("text", "") if message_content else ""
                else:
                    message = message_content
                
                # Создаём историю для агента
                agent_history = []
                for msg in history[:-1]:
                    content = msg.get("content", "")
                    if isinstance(content, list):
                        content = content[0].get("text", "") if content else ""
                    
                    if msg.get("role") == "user":
                        agent_history.append({"role": "user", "content": content})
                    elif msg.get("role") == "assistant":
                        agent_history.append({"role": "assistant", "content": content})
                
                # Определяем режим
                if mode == "auto":
                    detected_mode = detect_mode(message)
                else:
                    detected_mode = mode
                
                # Запускаем агента
                answer = run_agent(message, agent_history, SYSTEM_PROMPT, task=detected_mode)
                
                # Добавляем ответ в историю
                history.append({"role": "assistant", "content": answer})
                return history
            
            send_btn.click(
                fn=add_user_message,
                inputs=[msg_input, chatbot],
                outputs=[msg_input, chatbot]
            ).then(
                fn=bot_response,
                inputs=[chatbot, mode_selector],
                outputs=[chatbot]
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