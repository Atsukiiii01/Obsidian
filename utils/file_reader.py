from pathlib import Path

def read_file_bytes(path: str, size: int = 8192) -> bytes:
    path = Path(path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open("rb") as f:
        return f.read(size)
