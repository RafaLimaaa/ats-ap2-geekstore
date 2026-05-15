import sqlite3
import os

db_path = os.getenv("DB_PATH", "geekstore.db")

conn = sqlite3.connect(db_path)
conn.execute(
    "CREATE TABLE IF NOT EXISTS produtos "
    "(nome TEXT PRIMARY KEY, preco REAL, estoque INTEGER)"
)
# INSERT OR REPLACE garante stock cheio mesmo se o CI reaproveitar um DB de run anterior
conn.execute("INSERT OR REPLACE INTO produtos VALUES ('teclado', 200.0, 10)")
conn.execute("INSERT OR REPLACE INTO produtos VALUES ('mouse', 100.0, 5)")
conn.commit()
conn.close()
