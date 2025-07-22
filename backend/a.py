import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table_name in tables:
    print(f"\n--- Schema for table: {table_name[0]} ---")
    cursor.execute(f"PRAGMA table_info({table_name[0]});")
    for row in cursor.fetchall():
        print(f"{row[1]} ({row[2]})")

conn.close()
