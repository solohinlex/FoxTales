# src/embeddings.py
from config import EMBED


def get_embedding(text: str) -> list[float]:
    """
    Универсальная функция эмбеддинга.
    Провайдер задаётся через EMBED_PROVIDER в .env
    """
    provider = EMBED["provider"].lower()

    if provider == "ollama":
        return _embed_ollama(text)
    elif provider == "openai":
        return _embed_openai(text)
    else:
        raise ValueError(
            f"Неизвестный EMBED_PROVIDER: '{provider}'. "
            f"Доступные: ollama, openai"
        )


def _embed_ollama(text: str) -> list[float]:
    import ollama
    client = ollama.Client(host=EMBED["base_url"])
    response = client.embeddings(
        model=EMBED["model"],
        prompt=text
    )
    return response["embedding"]


def _embed_openai(text: str) -> list[float]:
    from openai import OpenAI
    client = OpenAI(
        api_key=EMBED["api_key"],
        base_url=EMBED.get("base_url") or None
    )
    response = client.embeddings.create(
        model=EMBED["model"],
        input=text
    )
    return response.data[0].embedding