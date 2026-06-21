# src/skills/characters.py
import os
import yaml
from .base import Skill, SkillResult

CONTENT_PATH = "./content"

class ListCharacters(Skill):
    name = "list_characters"
    description = "Получить список всех персонажей"
    parameters = {"type": "object", "properties": {}}

    def execute(self, **kwargs) -> SkillResult:
        path = os.path.join(CONTENT_PATH, "characters")
        chars = [f.replace('.yml', '') for f in sorted(os.listdir(path))]
        return SkillResult(True, "\n".join(chars))


class GetCharacter(Skill):
    name = "get_character"
    description = "Получить информацию о персонаже по имени файла"
    parameters = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Имя файла персонажа без расширения, например: tamamo"
            }
        },
        "required": ["name"]
    }

    def execute(self, name: str, **kwargs) -> SkillResult:
        path = os.path.join(CONTENT_PATH, "characters", f"{name}.yml")
        if not os.path.exists(path):
            return SkillResult(False, f"Персонаж не найден: {name}")
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        # Форматируем yml в читаемый текст
        result = f"# {name}\n\n"
        for key, val in data.items():
            result += f"**{key}**: {val}\n"
        return SkillResult(True, result)
