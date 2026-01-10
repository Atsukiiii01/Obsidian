import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "magic.db"

def match_signatures(file_bytes: bytes):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT file_type, hex_signature, offset, confidence
        FROM signatures
    """)

    matches = []

    for file_type, hex_sig, offset, confidence in cur.fetchall():
        sig_bytes = bytes.fromhex(hex_sig)
        end = offset + len(sig_bytes)

        if file_bytes[offset:end] == sig_bytes:
            matches.append((file_type, confidence))

    conn.close()
    return matches
