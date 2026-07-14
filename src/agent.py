# src/agent.py
import json
from litellm import completion
from skills import ALL_SKILLS, SKILLS_MAP
from config import MODEL
from prompts import Presets, PromptBuilder

def run_agent(
    user_message: str,
    history: list,
    system_prompt: str | None = None,
    task: str | None = None,
    variant: str = "default"
) -> str:
    """Запуск агента с поддержкой выбора промпта
    
    Args:
        user_message: Сообщение пользователя
        history: История диалога
        system_prompt: Системный промпт (для обратной совместимости)
        task: Название задачи для выбора пресета (analysis, editing, etc.)
        variant: Вариант промпта ("default" или "extract")
    
    Returns:
        Ответ агента
    """
    # Определяем промпт: либо из task, либо из system_prompt
    if task:
        prompt = Presets.for_task(task, variant)
    elif system_prompt:
        prompt = system_prompt
    else:
        prompt = Presets.for_task("search", variant)  # промпт по умолчанию
    
    history.append({"role": "user", "content": user_message})
    
    messages = [{"role": "system", "content": prompt}] + history
    tools = [skill.to_tool_dict() for skill in ALL_SKILLS]

    # Цикл: модель может вызвать несколько скиллов подряд
    while True:
        response = completion(
            model=MODEL["model"],
            api_key=MODEL["api_key"],
            api_base=MODEL["api_base"],
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Модель вызывает скилл
        if message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                skill_name = tool_call.function.name
                skill_args = json.loads(tool_call.function.arguments)

                print(f"  🔧 {skill_name}({skill_args})")

                skill = SKILLS_MAP.get(skill_name)
                if skill:
                    result = skill.execute(**skill_args)
                    content = result.content
                else:
                    content = f"Скилл не найден: {skill_name}"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": content
                })

        # Финальный ответ
        else:
            answer = message.content.strip()
            history.append({"role": "assistant", "content": answer})
            return answer
