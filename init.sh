#!/bin/bash
set -e

echo "🦊 FoxTales AI — инициализация..."

# Ждём готовности Ollama
echo "⏳ Ожидание запуска Ollama..."
OLLAMA_URL="http://ollama:11434"

until curl -s "${OLLAMA_URL}/api/tags" > /dev/null 2>&1; do
    echo "   Ждём Ollama..."
    sleep 2
done

echo "✅ Ollama готов!"

# Проверяем наличие модели
echo "📥 Проверка модели ${EMBED_MODEL:-nomic-embed-text}..."
if ! curl -s "${OLLAMA_URL}/api/tags" | grep -q "${EMBED_MODEL:-nomic-embed-text}"; then
    echo "   Загрузка модели..."
    curl -X POST "${OLLAMA_URL}/api/pull" -H "Content-Type: application/json" -d "{\"name\": \"${EMBED_MODEL:-nomic-embed-text}\"}"
    echo "✅ Модель загружена!"
else
    echo "✅ Модель уже установлена!"
fi

# Запуск веб-интерфейса
echo ""
echo "🚀 Запуск веб-интерфейса..."
echo "🌐 Веб-интерфейс будет доступен по адресу: http://localhost:${WEB_PORT:-7860}"
echo ""

exec python src/web.py