# src/skills/__init__.py
from .chapters import ListWorks, ListChapters, ReadChapter, ReadWorkNotes
from .characters import ListCharacters, GetCharacter
from .lore import ListLore, ReadLore, ListNotes, ReadNote
from .search import SearchContent

ALL_SKILLS = [
    ListWorks(),
    ListChapters(),
    ReadChapter(),
    ReadWorkNotes(),
    ListCharacters(),
    GetCharacter(),
    ListLore(),
    ReadLore(),
    ListNotes(),
    ReadNote(),
    SearchContent(),
]

SKILLS_MAP = {skill.name: skill for skill in ALL_SKILLS}