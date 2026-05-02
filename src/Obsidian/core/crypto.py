import hashlib
from pathlib import Path

def generate_hashes(file_path, chunk_size=65536):
    """Generates standard IOC hashes for threat intelligence lookups."""
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return {}

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    try:
        with path.open("rb") as f:
            while chunk := f.read(chunk_size):
                md5.update(chunk)
                sha1.update(chunk)
                sha256.update(chunk)
                
        return {
            "md5": md5.hexdigest(),
            "sha1": sha1.hexdigest(),
            "sha256": sha256.hexdigest()
        }
    except Exception:
        return {}