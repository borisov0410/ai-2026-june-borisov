import re

# Запрещённые паттерны (Input Guard)
FORBIDDEN_PATTERNS = [
    r"ignore\s+(previous|all)",
    r"забудь\s+(все|инструкции)",
    r"system\s+prompt|системн.*инструкц",
    r"base64|decode|декодир",
    r"\bdelete\b|\bupdate\b|\bdrop\b|\binsert\b",
    r"god\s*mode|admin\s*mode",
    r"шаг\s*1.*шаг\s*2" # Защита от многошагового выведывания
]

# Паттерны секретов для Output Guard (Redaction)
SECRET_PATTERNS = [
    r"sk-prod-[a-zA-Z0-9\-]+",
    r"super_secret_db_pass_\d+",
    r"admin_token_[a-zA-Z0-9]+",
    r"You are a QA Assistant"
]

def check_input_guard(user_input: str) -> tuple[bool, str]:
    """Проверяет ввод на наличие атак. Возвращает (is_safe, error_message)"""
    lower_input = user_input.lower()
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, lower_input, re.IGNORECASE):
            return False, "⛔ Access Denied: Запрос содержит запрещённые паттерны или попытки инъекции промпта."
    return True, ""

def apply_output_guard(response_text: str) -> str:
    """Цензурирует вывод, заменяя секреты и утечки промпта на [REDACTED]"""
    sanitized = response_text
    for pattern in SECRET_PATTERNS:
        sanitized = re.sub(pattern, "[REDACTED]", sanitized, flags=re.IGNORECASE)
    
    # Дополнительная проверка: если модель пытается выдать структуру БД с секретами
    if "secrets" in sanitized.lower() and ("key" in sanitized.lower() or "password" in sanitized.lower()):
        sanitized = "⛔ Access Denied: Попытка раскрытия конфиденциальной структуры данных заблокирована."
        
    return sanitized