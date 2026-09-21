"""Конфигурация pytest и фикстуры для тестирования."""
import pytest
import requests
import json
import os
from datetime import datetime

# URL агента и Ollama
AGENT_URL = os.getenv("AGENT_URL", "http://localhost:8001")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11435")

@pytest.fixture(scope="session")
def agent_url():
    """URL защищённого агента."""
    return AGENT_URL

@pytest.fixture(scope="session")
def ollama_url():
    """URL Ollama для LLM-as-judge."""
    return OLLAMA_URL

@pytest.fixture(scope="session")
def http_session():
    """HTTP-сессия для запросов."""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session

@pytest.fixture(scope="session", autouse=True)
def check_services(agent_url, ollama_url, http_session):
    """Проверка доступности сервисов перед тестами."""
    try:
        resp = http_session.get(f"{agent_url}/health", timeout=5)
        resp.raise_for_status()
        print(f"✅ Агент доступен: {agent_url}")
    except Exception as e:
        pytest.skip(f"Агент недоступен: {e}")
    
    try:
        resp = http_session.get(f"{ollama_url}/api/tags", timeout=5)
        resp.raise_for_status()
        print(f"✅ Ollama доступна: {ollama_url}")
    except Exception as e:
        print(f"⚠️ Ollama недоступна, LLM-as-judge будет отключён: {e}")

def send_chat_request(http_session, agent_url, message):
    """Отправляет запрос к агенту и возвращает ответ."""
    try:
        resp = http_session.post(
            f"{agent_url}/chat",
            json={"message": message},
            timeout=120
        )
        resp.raise_for_status()
        return resp.json()["response"]
    except Exception as e:
        return f"ERROR: {str(e)}"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для добавления метаданных в отчёт."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        # Добавляем информацию о payload в отчёт
        if hasattr(item, "callspec"):
            payload_data = item.callspec.params.get("payload_data", {})
            report.sections.append(("Payload Info", json.dumps(payload_data, ensure_ascii=False, indent=2)))

def pytest_sessionfinish(session, exitstatus):
    """Генерация Markdown-отчёта после завершения тестов."""
    if not hasattr(session, "config"):
        return
    
    # Собираем результаты
    results = []
    for item in session.items:
        if hasattr(item, "execution_result"):
            results.append(item.execution_result)
    
    if not results:
        return
    
    # Генерируем Markdown
    markdown_report = generate_markdown_report(results)
    
    # Сохраняем
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_file = os.path.join(reports_dir, f"report_{timestamp}.md")
    
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(markdown_report)
    
    print(f"\n📄 Markdown отчёт сохранён: {md_file}")

def generate_markdown_report(results):
    """Генерирует Markdown-отчёт из результатов тестов."""
    lines = [
        "# 🛡️ Отчёт о тестировании безопасности LLM-агента",
        "",
        f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Агент:** {AGENT_URL}",
        "",
        "---",
        "",
        "## 📊 Сводка",
        "",
    ]
    
    # Подсчёт результатов
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    
    lines.extend([
        f"- **Всего тестов:** {total}",
        f"- **✅ Успешно:** {passed}",
        f"- **❌ Провалено:** {failed}",
        f"- **Процент успеха:** {(passed/total*100):.1f}%",
        "",
        "---",
        "",
        "## 🔍 Детальные результаты",
        "",
    ])
    
    # Детали по каждому тесту
    for result in results:
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        lines.extend([
            f"### {result['test_id']}: {result['test_name']}",
            "",
            f"**Статус:** {status}",
            f"**Категория:** {result['category']}",
            f"**Ожидалось блокирование:** {'Да' if result['expected_block'] else 'Нет'}",
            "",
            "**Payload:**",
            f"```",
            result["payload"],
            f"```",
            "",
            "**Ответ агента:**",
            f"```",
            result["response"][:500] + ("..." if len(result["response"]) > 500 else ""),
            f"```",
            "",
            f"**Оценка безопасности:** {'🟢 Безопасно' if result['judge_result']['safe'] else '🔴 Небезопасно'}",
            f"**Причина:** {result['judge_result']['reason']}",
            f"**Уверенность:** {result['judge_result']['confidence']:.2f}",
            f"**Метод оценки:** {result['judge_result']['method']}",
            "",
            "---",
            "",
        ])
    
    return "\n".join(lines)