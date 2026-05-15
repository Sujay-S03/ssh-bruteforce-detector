import sqlite3

DB_NAME = "attacks.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT UNIQUE,
            attempts INTEGER,
            attack_time TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_attack(ip, attempts, attack_time):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if IP already exists
    cursor.execute("""
        SELECT * FROM attacks WHERE ip_address = ?
    """, (ip,))

    existing = cursor.fetchone()

    if existing:

        # Update existing row
        cursor.execute("""
            UPDATE attacks
            SET attempts = ?, attack_time = ?
            WHERE ip_address = ?
        """, (attempts, attack_time, ip))

    else:

        # Insert new row
        cursor.execute("""
            INSERT INTO attacks (ip_address, attempts, attack_time)
            VALUES (?, ?, ?)
        """, (ip, attempts, attack_time))

    conn.commit()
    conn.close()