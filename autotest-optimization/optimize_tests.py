import ollama
import re
import os

# Исходный код автотестов (с исправленными отступами для корректного анализа)
ORIGINAL_CODE = """
import pytest
import requests

BASE_URL = "http://localhost:8000"

def test_create_user():
    payload = {"name": "Alice", "email": "alice@example.com"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"

def test_create_user_other_name():
    payload = {"name": "Bob", "email": "bob@example.com"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Bob"

def test_create_user_new_new_name():
    payload = {"name": "Charlie", "email": "charlie@example.com"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Charlie"

def test_create_user_invalid_email():
    payload = {"name": "Test", "email": "bad-email"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 400

def test_create_user_missing_name():
    payload = {"email": "test@example.com"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 400
"""

def main():
    model_name = "qwen2.5-coder"
    
    prompt = f"""
    Ты опытный QA-инженер и Senior Python-разработчик.
    Проанализируй следующий код автотестов на pytest:

    ```python
    {ORIGINAL_CODE}
    ```

    Твоя задача:
    1. Написать подробный код-ревью в формате Markdown. Обязательно выдели:
       - ✅ Что сделано хорошо (сильные стороны).
       - ❌ Что сделано плохо (слабые стороны, например: дублирование кода, нарушение DRY, отсутствие параметризации, хардкод, недостаточная проверка ошибок).
    2. Написать оптимизированный вариант этого кода, используя лучшие практики pytest:
       - Используй `@pytest.mark.parametrize` для устранения дублирования.
       - Используй фикстуры (fixtures) для повторяющихся данных или настроек.
       - Добавь аннотации типов и docstrings.
       - Улучши проверки (asserts) для негативных сценариев (например, проверка текста ошибки).

    Формат ответа строго такой:
    Сначала выведи раздел "## Код-ревью", а затем раздел "## Оптимизированный код", внутри которого должен быть только один блок кода с разметкой ```python ... ```.
    """

    print(f"🔄 Запрос к модели {model_name}... Это может занять некоторое время.")
    
    try:
        response = ollama.chat(model=model_name, messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        result = response['message']['content']
        
        # 1. Сохраняем полный отчёт в review.md
        with open("review.md", "w", encoding="utf-8") as f:
            f.write(result)
        print("✅ Отчёт успешно сохранён в файл: review.md")
        
        # 2. Извлекаем оптимизированный код в отдельный файл
        code_match = re.search(r'```python\s*(.*?)\s*```', result, re.DOTALL | re.IGNORECASE)
        if code_match:
            optimized_code = code_match.group(1).strip()
            with open("test_users_optimized.py", "w", encoding="utf-8") as f:
                f.write(optimized_code)
            print("✅ Оптимизированный код сохранён в файл: test_users_optimized.py")
        else:
            print("⚠️ Не удалось извлечь блок кода Python из ответа модели. Проверьте review.md вручную.")
            
    except Exception as e:
        print(f"❌ Ошибка при обращении к Ollama: {e}")
        print("Убедитесь, что Ollama запущена и модель загружена (ollama pull qwen2.5-coder)")

if __name__ == "__main__":
    main()