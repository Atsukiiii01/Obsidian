import sqlite3
from pathlib import Path

# Force the path to be absolute based on this file's location
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "magic.db"

_CACHE = None

def load_signatures():
    global _CACHE
    if _CACHE is not None:
        return _CACHE

    if not DB_PATH.exists():
        print(f"[!] ERROR: Database not found at {DB_PATH}")
        return []

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT file_type, hex_signature, offset, confidence FROM signatures")
            rows = cursor.fetchall()
            _CACHE = [
                (t, bytes.fromhex(h), o, c) 
                for t, h, o, c in rows
            ]
            print(f"[*] SUCCESS: Loaded {len(_CACHE)} signatures into RAM.")
        return _CACHE
    except Exception as e:
        print(f"[!] DATABASE ERROR: {e}")
        return []

def match_signatures(header, footer):
    signatures = load_signatures()
    hits = []

    for f_type, sig, offset, conf in signatures:
        if offset >= 0:
            end = offset + len(sig)
            if len(header) >= end and header[offset:end] == sig:
                hits.append((f_type, conf))
        else:
            # Check for signatures at the end of the file (like 'koly')
            if sig in footer:
                hits.append((f_type, conf))
    return hits