import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "magic.db"


def match_signatures(file_bytes):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT file_type, hex_signature, offset, confidence FROM signatures"
    )

    hits = []

    for file_type, hex_sig, offset, confidence in cursor.fetchall():
        sig = bytes.fromhex(hex_sig)
        end = offset + len(sig)

        if file_bytes[offset:end] == sig:
            hits.append((file_type, confidence))

    conn.close()
    return hits
