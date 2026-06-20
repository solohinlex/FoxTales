# FoxTales

Репозиторий авторской вселенной [«Лисьих сказок»](https://author.today/u/solohinlex)
Алексея Солохина.

Одновременно — эксперимент по организации работы с литературными текстами
через нейросети: справка, бета-ридинг, быстрый поиск и другая вспомогательная работа.

---

## ⚖️ Лицензия и правила

Все лицензионные документы хранятся в основном репозитории профиля.
Перед использованием материалов, пожалуйста, ознакомьтесь с ними:

- **[Условия лицензирования](https://github.com/solohinlex/solohinlex/blob/main/LICENSE.md)** —
  двойная лицензия: скрипты открыты под **MIT**, литературные тексты защищены
  авторским правом. Тексты можно копировать и адаптировать с указанием автора,
  коммерческое использование — только с разрешения.

- **[Руководство по участию](https://github.com/solohinlex/solohinlex/blob/main/CONTRIBUTING.md)** —
  как предложить исправление, добавить скрипт или текст через Pull Request.

- **[Политика безопасности](https://github.com/solohinlex/solohinlex/blob/main/SECURITY.md)** —
  как сообщить об уязвимости напрямую, минуя публичные обсуждения.

- **[Кодекс поведения](https://github.com/solohinlex/solohinlex/blob/main/CODE_OF_CONDUCT.md)** —
  правила общения внутри проекта.

---

## 🚀 Быстрый старт

### Требования

- WSL2 / Linux
- Python 3.12+
- [Ollama](https://ollama.com/) — установлен и запущен локально? либо доступен OpenAI api

---

### 1. Подготовка окружения

```bash
# Необходимые пакеты для Python
sudo apt-get update
sudo apt install python3-pip python3.12-venv -y

# Клонируем репозиторий
git clone https://github.com/solohinlex/FoxTales.git
cd FoxTales

# Создаём окружение и устанавливаем зависимости
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Настройка

```bash
cp .env.example .env
nano .env
```

> Для работы через Ollama укажи локальный адрес в `API_BASE`,
> например `http://localhost:11434`

### 3. Первый запуск

```bash
source .venv/bin/activate
python src/main.py
```

### 4. Повторный запуск

```bash
cd FoxTales
source .venv/bin/activate
python src/main.py
```

---

## Контакты

По вопросам коммерческого использования текстов или сотрудничества:

- **Email:** [solohinlex@gmail.com](mailto:solohinlex@gmail.com)
- **Telegram:** [@Solohinlex](https://t.me/Solohinlex)
