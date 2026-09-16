# LLM Agent Security Demo (Pentest Environment)

Демонстрационная среда для тестирования уязвимостей LLM-агента с намеренно ослабленной защитой. Проект создан исключительно в образовательных целях для демонстрации атак из **OWASP Top 10 for LLM**.

> ⚠️ **ВНИМАНИЕ:** Не используйте этот код в production-среде! Он содержит намеренные уязвимости (отсутствие RBAC, слабые промпты, избыточные права инструментов).

## 🏗️ Архитектура стенда
- **API:** FastAPI (Python 3.11)
- **Agent Framework:** LlamaIndex (ReAct Agent)
- **LLM Backend:** Ollama (модель `qwen2.5:7b`)
- **Storage:** SQLite (таблицы: `clients`, `orders`, `secrets`)
- **RAG:** Векторный поиск по внутренним документам (`/app/data/docs/`)

## 📋 Предварительные требования
- Установленный [Docker Desktop](https://www.docker.com/products/docker-desktop/) (с выделенной памятью не менее 4-8 ГБ).
- Установленный [VS Code](https://code.visualstudio.com/) с расширениями: *Docker*, *REST Client* (или используйте встроенный Swagger).

## 🚀 Пошаговый запуск

### 1. Сборка и запуск контейнеров
Откройте терминал в корневой папке проекта и выполните:
```bash
docker compose up --build -d

### 2. Загрузка LLM-модели
bash docker exec ollama ollama pull qwen2.5:7b

### 3. Прогрев модели (Warmup)
Поскольку модель работает на CPU, первый запрос может занять до 2 минут (загрузка весов в RAM). Чтобы избежать таймаутов при первом тестировании, выполните "прогрев":
bash
# Для Windows PowerShell используйте curl.exe:
curl.exe http://localhost:8000/warmup

### Остановка и очистка
# Остановка контейнеров
docker compose down

# Полная очистка (включая тома с БД и моделями)
docker compose down -v 