from .loader import (
    load_prompt,
    PromptBuilder,
    Presets,
    get_system_prompt,
)

# Для обратной совместимости
SYSTEM_PROMPT = get_system_prompt()

# Экспорт основных функций
__all__ = [
    "load_prompt",
    "PromptBuilder",
    "Presets",
    "get_system_prompt",
    "SYSTEM_PROMPT",
]
