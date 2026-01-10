import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "magic.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS signatures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_type TEXT NOT NULL,
        hex_signature TEXT NOT NULL,
        offset INTEGER NOT NULL,
        confidence REAL DEFAULT 0.95
    )
    """)

    cur.execute("DELETE FROM signatures")

    signatures = [
        ("PDF", "25504446", 0),
        ("PNG", "89504E470D0A1A0A", 0),
        ("JPG", "FFD8FF", 0),
        ("GIF", "47494638", 0),
        ("ZIP", "504B0304", 0),
        ("RAR", "52617221", 0),
        ("MP3", "494433", 0),
        ("MP3", "FFFB", 0),
        ("MP4", "6674797069736F6D", 4),
        ("MP4", "667479704D534E56", 4),
        ("EXE", "4D5A", 0),
    ]

    cur.executemany("""
    INSERT INTO signatures (file_type, hex_signature, offset)
    VALUES (?, ?, ?)
    """, signatures)

    conn.commit()
    conn.close()

    print(" SQLite signature database initialized successfully")

if __name__ == "__main__":
    init_db()
