import sqlite3
from pathlib import Path

# Ensure paths are relative to project root
DB_DIR = Path("src/Obsidian/database")
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "magic.db"

def setup():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # WE MUST DROP THE OLD FLAWED TABLE
    cursor.execute("DROP TABLE IF EXISTS signatures")
    cursor.execute("""
    CREATE TABLE signatures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_type TEXT NOT NULL,
        hex_signature TEXT NOT NULL,
        offset INTEGER DEFAULT 0,
        confidence REAL DEFAULT 1.0
    )
    """)

    # Exactly 8 Master Signatures
    signatures = [
        ('Apple Disk Image (UDIF)', '6b6f6c79', -512, 1.0), # Footer search
        ('Zlib (Best)', '78DA', 0, 0.9),
        ('Zlib (Default)', '789C', 0, 0.9),
        ('PNG', '89504E470D0A1A0A', 0, 1.0),
        ('JPEG', 'FFD8FF', 0, 0.95),
        ('PDF', '25504446', 0, 1.0),
        ('ELF Binary', '7F454C46', 0, 1.0),
        ('Mach-O ARM64', 'CFFAEDFE', 0, 1.0)
    ]

    cursor.executemany(
        "INSERT INTO signatures (file_type, hex_signature, offset, confidence) VALUES (?, ?, ?, ?)",
        signatures
    )

    conn.commit()
    conn.close()
    print(f"[*] Intelligence Vault Seeded: {DB_PATH}")

if __name__ == "__main__":
    setup()