# Database creation
import sqlite3

def init_db():
    # DB creation
    table = sqlite3.connect("database.db")
    # Execute schema
    with open("schema.sql") as f:
        table.executescript(f.read())
    table.commit()
    table.close()

if __name__ == "__main__":
    init_db()
    print("Database created correctly")
