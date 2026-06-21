# src/skills/base.py
from dataclasses import dataclass
from typing import Any

@dataclass
class SkillResult:
    success: bool
    content: str

class Skill:
    name: str
    description: str
    parameters: dict  # JSON Schema для параметров

    def execute(self, **kwargs) -> SkillResult:
        raise NotImplementedError

    def to_tool_dict(self) -> dict:
        """Конвертирует скилл в формат OpenAI tools"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
