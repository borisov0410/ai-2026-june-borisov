import sqlite3
import os

DB_PATH = "/app/data/database.db"

def init_database():
    """Initialize SQLite database with sample data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            status TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            client_id INTEGER,
            amount REAL,
            status TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secrets (
            id INTEGER PRIMARY KEY,
            key TEXT,
            value TEXT,
            description TEXT
        )
    """)
    
    # Insert sample data
    cursor.executemany("INSERT OR IGNORE INTO clients VALUES (?, ?, ?, ?)", [
        (1, "Alice Johnson", "alice@example.com", "active"),
        (2, "Bob Smith", "bob@example.com", "inactive"),
        (3, "Charlie Brown", "charlie@example.com", "active"),
    ])
    
    cursor.executemany("INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?)", [
        (1, 1, 1500.50, "completed"),
        (2, 1, 2300.00, "pending"),
        (3, 2, 800.75, "completed"),
        (4, 3, 3200.00, "shipped"),
    ])
    
    cursor.executemany("INSERT OR IGNORE INTO secrets VALUES (?, ?, ?, ?)", [
        (1, "API_KEY", "sk-prod-12345-abcde-67890", "Production API key"),
        (2, "DB_PASSWORD", "super_secret_db_pass_2024", "Database password"),
        (3, "ADMIN_TOKEN", "admin_token_xyz789", "Admin authentication token"),
    ])
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    init_database()