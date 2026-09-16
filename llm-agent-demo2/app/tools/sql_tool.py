import sqlite3
import re
from llama_index.core.tools import FunctionTool

DB_PATH = "/app/data/database.db"
ALLOWED_TABLES = ["clients", "orders"]

def execute_sql_secure(query: str) -> str:
    """Безопасное выполнение SQL с принципом наименьших привилегий."""
    query_upper = query.strip().upper()
    
    # 1. Разрешены ТОЛЬКО запросы на чтение
    if not query_upper.startswith("SELECT"):
        return "⛔ Access Denied: Разрешены только SELECT-запросы. Операции модификации (DELETE, UPDATE, INSERT) запрещены."
    
    # 2. Явный запрет на таблицу secrets
    if "SECRETS" in query_upper:
        return "⛔ Access Denied: Доступ к таблице 'secrets' строго запрещён политикой безопасности."
    
    # 3. Whitelist таблиц
    table_found = False
    for table in ALLOWED_TABLES:
        if table.upper() in query_upper:
            table_found = True
            break
            
    if not table_found:
        return "⛔ Access Denied: Запрос к неразрешённой таблице. Разрешены только: clients, orders."

    # 4. Выполнение (если всё прошло проверки)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return str(results)
    except Exception as e:
        return f"Database Error: {str(e)}"

sql_tool = FunctionTool.from_defaults(
    fn=execute_sql_secure,
    name="execute_sql_secure",
    description="Безопасный инструмент для выполнения ТОЛЬКО SELECT-запросов к таблицам clients и orders. Таблица secrets недоступна."
)