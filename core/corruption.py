from pathlib import Path

def corruption_hints(
    file_path: str,
    detected_type: str,
    file_bytes: bytes,
    entropy: float
):
    hints = []

    size = len(file_bytes)

    # --- Generic suspicious cases ---
    if size < 16:
        hints.append("File is extremely small – likely truncated")

    # --- Type-specific heuristics ---
    if detected_type == "MP4":
        if b"ftyp" not in file_bytes[:64]:
            hints.append("MP4 container header incomplete or missing")

    elif detected_type == "MKV":
        if not file_bytes.startswith(b"\x1A\x45\xDF\xA3"):
            hints.append("MKV EBML header missing or corrupted")

    elif detected_type == "ZIP":
        if b"PK\x05\x06" not in file_bytes[-64:]:
            hints.append("ZIP end-of-central-directory record missing")

    elif detected_type in ("BINARY", "UNKNOWN"):
        if entropy > 7.8:
            hints.append("High entropy binary – possible compressed or encrypted data")

    # --- Confidence-based hint ---
    if entropy < 1.0:
        hints.append("Very low entropy – file may contain mostly null data")

    return hints
