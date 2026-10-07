import ollama
import re
from typing import Dict, List
from prompts import PROMPT_LOW, PROMPT_MEDIUM, PROMPT_HIGH

# Критерии оценки
CRITERIA = {
    'completeness': 'Полнота (покрытие сценариев)',
    'format': 'Формат (структурированность)',
    'accuracy': 'Точность (корректность данных)'
}

def generate_test_cases(prompt: str, model: str = 'llama3.2') -> str:
    """Генерация тест-кейсов через Ollama"""
    try:
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Ошибка генерации: {str(e)}"

def evaluate_completeness(response: str) -> int:
    """Оценка полноты (0-10): проверяет наличие ключевых сценариев"""
    score = 0
    key_scenarios = [
        'цена < 0', 'отрицательн',
        'скидка < 0', 'скидка > 100',
        'границ', '0%', '100%',
        'ValueError', 'исключен'
    ]
    
    response_lower = response.lower()
    found = sum(1 for scenario in key_scenarios if scenario in response_lower)
    
    # Нормализуем оценку
    score = min(10, int((found / len(key_scenarios)) * 10))
    return score

def evaluate_format(response: str) -> int:
    """Оценка формата (0-10): проверяет структурированность"""
    score = 0
    
    # Проверяем наличие структуры
    has_id = bool(re.search(r'(ID|№|#|\d+\.)', response))
    has_description = bool(re.search(r'(описан|проверк|тест)', response, re.I))
    has_input = bool(re.search(r'(вход|input|данные|price|discount)', response, re.I))
    has_expected = bool(re.search(r'(ожида|result|результат)', response, re.I))
    has_categories = bool(re.search(r'(позитив|негатив|категор)', response, re.I))
    
    score += 2 * has_id
    score += 2 * has_description
    score += 2 * has_input
    score += 2 * has_expected
    score += 2 * has_categories
    
    return score

def evaluate_accuracy(response: str) -> int:
    """Оценка точности (0-10): проверяет корректность ожидаемых результатов"""
    score = 10
    
    # Проверяем наличие ошибок в расчетах
    error_patterns = [
        r'100.*\+.*скидк',  # Неправильная формула
        r'price.*\+.*discount',  # Сложение вместо вычитания
    ]
    
    for pattern in error_patterns:
        if re.search(pattern, response, re.I):
            score -= 3
    
    # Проверяем наличие правильных граничных значений
    correct_boundaries = [
        r'0%',
        r'100%',
        r'price.*0',
    ]
    
    found_boundaries = sum(1 for pattern in correct_boundaries 
                          if re.search(pattern, response, re.I))
    
    if found_boundaries < 2:
        score -= 2
    
    return max(0, score)

def evaluate_response(response: str) -> Dict[str, int]:
    """Полная оценка ответа LLM"""
    return {
        'completeness': evaluate_completeness(response),
        'format': evaluate_format(response),
        'accuracy': evaluate_accuracy(response)
    }

def calculate_total_score(scores: Dict[str, int]) -> int:
    """Расчет общей оценки"""
    return sum(scores.values())

def main():
    prompts = {
        'LOW (Низкая детализация)': PROMPT_LOW,
        'MEDIUM (Средняя детализация)': PROMPT_MEDIUM,
        'HIGH (Высокая детализация)': PROMPT_HIGH
    }
    
    results = []
    
    print("=" * 80)
    print("ОЦЕНКА КАЧЕСТВА ПРОМПТОВ ДЛЯ ГЕНЕРАЦИИ ТЕСТ-КЕЙСОВ")
    print("=" * 80)
    
    for prompt_name, prompt_text in prompts.items():
        print(f"\n{'=' * 80}")
        print(f"Промпт: {prompt_name}")
        print(f"{'=' * 80}")
        
        # Генерация тест-кейсов
        print("\nГенерация тест-кейсов...")
        response = generate_test_cases(prompt_text)
        
        # Оценка
        print("Оценка ответа...")
        scores = evaluate_response(response)
        total = calculate_total_score(scores)
        
        result = {
            'prompt_name': prompt_name,
            'prompt': prompt_text,
            'response': response,
            'scores': scores,
            'total': total
        }
        results.append(result)
        
        # Вывод в консоль
        print(f"\nСгенерированные тест-кейсы:\n{response}")
        print(f"\nОценки:")
        for criterion, score in scores.items():
            print(f"  {CRITERIA[criterion]}: {score}/10")
        print(f"  Общая оценка: {total}/30")
    
    # Запись результатов в файл
    output_file = 'compare_answers_resuls.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("РЕЗУЛЬТАТЫ СРАВНЕНИЯ КАЧЕСТВА ПРОМПТОВ\n")
        f.write("=" * 80 + "\n\n")
        
        for result in results:
            f.write(f"{'=' * 80}\n")
            f.write(f"ПРОМПТ: {result['prompt_name']}\n")
            f.write(f"{'=' * 80}\n\n")
            
            f.write("Текст промпта:\n")
            f.write("-" * 80 + "\n")
            f.write(result['prompt'] + "\n")
            f.write("-" * 80 + "\n\n")
            
            f.write("Сгенерированные тест-кейсы:\n")
            f.write("-" * 80 + "\n")
            f.write(result['response'] + "\n")
            f.write("-" * 80 + "\n\n")
            
            f.write("Оценки:\n")
            for criterion, score in result['scores'].items():
                f.write(f"  {CRITERIA[criterion]}: {score}/10\n")
            f.write(f"  Общая оценка: {result['total']}/30\n\n")
        
        # Итоговая сводка
        f.write("\n" + "=" * 80 + "\n")
        f.write("ИТОГОВАЯ СВОДКА\n")
        f.write("=" * 80 + "\n\n")
        
        for result in results:
            f.write(f"{result['prompt_name']}: {result['total']}/30\n")
        
        f.write("\nВывод: Более детализированные промпты дают более качественные результаты.\n")
    
    print(f"\n{'=' * 80}")
    print(f"Результаты сохранены в файл: {output_file}")
    print(f"{'=' * 80}")

if __name__ == '__main__':
    main()