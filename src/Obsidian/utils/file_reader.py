from pathlib import Path

def read_file_segments(path, head_size=8192, tail_size=512):
    """Reads both the start and end of a file for deep forensic analysis."""
    file_path = Path(path).expanduser().resolve()
    if not file_path.exists():
        return b"", b""

    try:
        with file_path.open("rb") as f:
            header = f.read(head_size)
            
            f.seek(0, 2) # Jump to end
            file_size = f.tell()
            
            if file_size <= head_size:
                return header, b""
                
            f.seek(max(0, file_size - tail_size))
            footer = f.read(tail_size)
            return header, footer
    except Exception:
        return b"", b""

def is_probably_text(raw_bytes):
    """Heuristic to check if data is human-readable."""
    if not raw_bytes or b'\x00' in raw_bytes:
        return False
    printable = sum(1 for b in raw_bytes if 32 <= b <= 126 or b in (9, 10, 13))
    return (printable / len(raw_bytes)) > 0.85 if raw_bytes else False