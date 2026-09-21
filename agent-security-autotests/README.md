# 🛡️ Automated Security Testing for LLM Agent

Автоматизированный фреймворк для тестирования безопасности защищённого LLM-агента (`llm-agent-demo2`).

## 📋 Возможности

- ✅ **20 тестовых payloads** (15 негативных + 5 позитивных)
- ✅ **Категории атак:** Encoding, Jailbreak, Indirect Injection, Exfiltration, Manipulation
- ✅ **LLM-as-judge** для интеллектуальной оценки ответов
- ✅ **Эвристическая проверка** для быстрых тестов
- ✅ **Множественные форматы отчётов:** JSON, HTML, Markdown
- ✅ **Параллельное выполнение** тестов

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
cd agent-security-autotests
pip install -r requirements.txt

### 2. Запуск тестов
# Запуск всех тестов
pytest

# Запуск только негативных тестов (атаки)
pytest -m negative

# Запуск только позитивных тестов (легитимные запросы)
pytest -m positive

# Запуск с подробным выводом
pytest -v -s

# Запуск конкретных категорий
pytest -k "encoding or jailbreak"

###3. Просмотр отчётов
После выполнения тестов отчёты сохраняются в папку reports/:
report.html — интерактивный HTML-отчёт (откройте в браузере)
report.json — машиночитаемый JSON-отчёт
report_YYYYMMDD_HHMMSS.md — Markdown-отчёт с временной меткой

# Открыть HTML-отчёт
start reports/report.html

