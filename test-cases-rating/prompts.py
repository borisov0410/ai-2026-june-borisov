# Три промпта разного уровня детализации для тестирования функции calculate_discount

PROMPT_LOW = """
Напиши тест-кейсы для функции calculate_discount.
"""

PROMPT_MEDIUM = """
Напиши тест-кейсы для функции calculate_discount в формате:
- ID
- Описание
- Входные данные
- Ожидаемый результат

Функция:
def calculate_discount(price, discount_percent):
    if price < 0:
        raise ValueError("Цена не может быть отрицательной")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Процент скидки должен быть от 0 до 100")
    return price * (1 - discount_percent / 100)
"""

PROMPT_HIGH = """
Напиши тест-кейсы для функции calculate_discount.

Раздели тест-кейсы на две категории:
1. Позитивные сценарии (корректные входные данные)
2. Негативные сценарии (некорректные входные данные, вызывающие исключения)

Формат каждого тест-кейса:
- ID: уникальный идентификатор
- Категория: позитивный/негативный
- Описание: что проверяется
- Входные данные: price, discount_percent
- Ожидаемый результат: возвращаемое значение или тип исключения

Функция:
def calculate_discount(price, discount_percent):
    if price < 0:
        raise ValueError("Цена не может быть отрицательной")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Процент скидки должен быть от 0 до 100")
    return price * (1 - discount_percent / 100)

Обязательно включи граничные значения: 0, 100, отрицательные числа.
"""