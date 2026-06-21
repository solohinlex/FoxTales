.DEFAULT_GOAL := help

# ─── Конфигурация ─────────────────────────────────────────
VENV        ?= .venv
PYTHON      ?= $(VENV)/bin/python
PIP         ?= $(VENV)/bin/pip
SRC         ?= src/main.py
WEB         ?= src/web.py

export PYTHONIOENCODING = utf-8
export PYTHONUTF8       = 1

# ─── Окружение ────────────────────────────────────────────
.PHONY: venv
venv: ## Создаёт виртуальное окружение
	@if [ ! -d "$(VENV)" ]; then \
		python3 -m venv $(VENV); \
		echo "✅ Окружение создано: $(VENV)"; \
	else \
		echo "ℹ️  Окружение уже существует, пропускаю"; \
	fi

.PHONY: install
install: venv ## Устанавливает зависимости из requirements.txt
	$(PIP) install -r requirements.txt
	@echo "✅ Зависимости установлены"

.PHONY: setup
setup: install ## Первичная настройка: venv + deps + .env (make setup)
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Создан .env — отредактируй его перед запуском"; \
	else \
		echo "ℹ️  .env уже существует, пропускаю"; \
	fi

# ─── Запуск ───────────────────────────────────────────────
.PHONY: run
run: ## Запускает бота (make run)
	$(PYTHON) $(SRC)

.PHONY: web
web: ## Запускает веб-интерфейс (make web)
	$(PYTHON) $(WEB)

# ─── Git ──────────────────────────────────────────────────
.PHONY: push
push: ## Коммит + push (make push M="сообщение")
	@if [ -z "$(M)" ]; then \
		echo "❌ Укажите сообщение: make push M=\"ваше сообщение\""; \
		exit 1; \
	fi
	@echo "📝 Коммит: $(M)"
	@git add .
	@git commit -m "$(M)" || echo "ℹ️  Нет изменений для коммита"
	@echo "🚀 Пуш..."
	@git push origin $$(git branch --show-current)
	@echo "✅ Готово!"

# ─── Утилиты ──────────────────────────────────────────────
.PHONY: freeze
freeze: ## Сохраняет текущие зависимости в requirements.txt
	$(PIP) freeze > requirements.txt
	@echo "✅ requirements.txt обновлён"

.PHONY: clean
clean: ## Удаляет виртуальное окружение и кэш
	rm -rf $(VENV) $$(find . -type d -name __pycache__)
	@echo "✅ Окружение удалено"

# ─── Help ─────────────────────────────────────────────────
.PHONY: help
help: ## Показывает это сообщение
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

.PHONY: run-debug
run-debug: ## Отладка окружения
	@echo "LANG=$$LANG"
	@echo "LC_ALL=$$LC_ALL"
	@echo "PYTHONIOENCODING=$$PYTHONIOENCODING"