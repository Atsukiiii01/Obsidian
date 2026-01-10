import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "magic.db"

def learn_signature(
    file_path: str,
    file_bytes: bytes,
    correct_type: str,
    offset: int = 0,
    length: int = 8,
    confidence: float = 0.9
):
    """
    Extracts magic bytes from a file and stores them in SQLite.
    """

    signature_bytes = file_bytes[offset:offset + length]
    hex_signature = signature_bytes.hex().upper()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # prevent duplicates
    cur.execute("""
        SELECT 1 FROM signatures
        WHERE file_type=? AND hex_signature=? AND offset=?
    """, (correct_type, hex_signature, offset))

    if cur.fetchone():
        conn.close()
        print(" Signature already exists. Skipping.")
        return False

    cur.execute("""
        INSERT INTO signatures (file_type, hex_signature, offset, confidence)
        VALUES (?, ?, ?, ?)
    """, (correct_type, hex_signature, offset, confidence))

    conn.commit()
    conn.close()

    print(f" Learned new signature for {correct_type}: {hex_signature} @ offset {offset}")
    return True
