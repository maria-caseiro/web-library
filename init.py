import sqlite3
import secrets
import os

# Create .env file with SECRET_KEY
if not os.path.exists(".env"):
    with open(".env", "w") as f:
        f.write(f"SECRET_KEY={secrets.token_hex(32)}")
    print(".env created with random SECRET_KEY.")

# Create data directory
os.makedirs("data", exist_ok=True)

# Create database and run schema+seed SQL scripts
with sqlite3.connect("data/library.db") as conn:
    with open("schema.sql", encoding="utf-8") as f:
        conn.executescript(f.read())
    with open("seed.sql", encoding="utf-8") as f:
        conn.executescript(f.read())

print("Database created successfully.")