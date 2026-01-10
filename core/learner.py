import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "magic.db"


def learn_signature(
    file_path,
    file_bytes,
    correct_type,
    offset=0,
    length=8,
    confidence=0.9
):
    signature = file_bytes[offset:offset + length]
    hex_sig = signature.hex().upper()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM signatures WHERE file_type=? AND hex_signature=? AND offset=?",
        (correct_type, hex_sig, offset)
    )

    if cursor.fetchone():
        conn.close()
        print("Signature already exists, skipping")
        return False

    cursor.execute(
        "INSERT INTO signatures (file_type, hex_signature, offset, confidence) "
        "VALUES (?, ?, ?, ?)",
        (correct_type, hex_sig, offset, confidence)
    )

    conn.commit()
    conn.close()

    print(f"Learned new signature for {correct_type}: {hex_sig} @ offset {offset}")
    return True
