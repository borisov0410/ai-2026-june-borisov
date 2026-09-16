import sqlite3
from llama_index.core.tools import FunctionTool

DB_PATH = "/app/data/database.db"

def execute_sql(query: str) -> str:
    """Execute SQL query on internal database.
    
    Args:
        query: SQL query to execute
    
    Returns:
        Query results as string
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            conn.close()
            return str(results)
        else:
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            return f"Query executed successfully. Rows affected: {affected}"
    except Exception as e:
        return f"Error executing query: {str(e)}"

sql_tool = FunctionTool.from_defaults(
    fn=execute_sql,
    name="execute_sql",
    description="Execute SQL queries on internal database (clients, orders, secrets tables)"
)