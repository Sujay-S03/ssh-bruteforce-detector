import sqlite3

DB_NAME = "attacks.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            attempts INTEGER
        )
    """)

    conn.commit()
    conn.close()


def save_attack(ip, attempts):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attacks (ip_address, attempts)
        VALUES (?, ?)
    """, (ip, attempts))

    conn.commit()
    conn.close()