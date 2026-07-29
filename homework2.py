import argparse
import sys
import ollama

def generate_scenarios(num_scenarios, model_name):
    """
    Отправляет запрос в Ollama для генерации тест-кейсов.
    """
    prompt = f"""Ты — опытный QA-инженер.
Тебе необходимо написать СТРОГО {num_scenarios} сценариев тестирования для формы регистрации пользователя.

Поля формы:
1. Поле ввода имени пользователя
2. Поле ввода пароля
3. Поле ввода подтверждения пароля
4. Кнопка «Зарегистрировать»

Требования к сценариям:
- Набор должен включать как позитивные, так и негативные сценарии.
- Сценарии должны быть логичными и покрывать разные граничные значения, ошибки валидации и UX-аспекты (например, несовпадение паролей, пустые поля, спецсимволы, слишком короткие/длинные данные).

Формат вывода:
- Строго в формате Markdown. 
- Используй заголовки (H2 или H3) для каждого сценария, списки для шагов и ожидаемых результатов.
- ВАЖНО: НЕ пиши никаких вводных фраз (например, "Вот ваши сценарии") или заключительных слов. Выведи ТОЛЬКО чистый Markdown-код.
"""

    try:
        # Используем chat API для получения структурированного ответа
        response = ollama.chat(model=model_name, messages=[
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content']
    except ollama.ResponseError as e:
        print(f"Ошибка Ollama: {e.error}")
        sys.exit(1)
    except Exception as e:
        print(f"Неизвестная ошибка при обращении к Ollama: {e}")
        print("Убедитесь, что Ollama запущена и модель скачана.")
        sys.exit(1)

def main():
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(
        description="Генерация сценариев тестирования формы регистрации с помощью Ollama."
    )
    parser.add_argument(
        "-n", "--num", 
        type=int, 
        required=True, 
        help="Количество генерируемых сценариев (обязательный аргумент)."
    )
    parser.add_argument(
        "-m", "--model", 
        type=str, 
        default="llama3", 
        help="Имя модели Ollama (по умолчанию: llama3)."
    )
    
    args = parser.parse_args()

    if args.num <= 0:
        print("Ошибка: количество сценариев должно быть больше нуля.")
        sys.exit(1)

    print(f"Генерация {args.num} сценариев с использованием модели '{args.model}'...")
    print("Это может занять некоторое время в зависимости от вашего железа...")
    
    # Генерация
    markdown_content = generate_scenarios(args.num, args.model)

    # Сохранение в файл
    output_file = "test_scenarios.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"\nГотово! Сценарии успешно сгенерированы и сохранены в файл: {output_file}")

if __name__ == "__main__":
    main()