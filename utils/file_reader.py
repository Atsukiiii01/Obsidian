from pathlib import Path


def read_file_bytes(path, size=8192):
    file_path = Path(path).expanduser().resolve()

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with file_path.open("rb") as file:
        return file.read(size)
