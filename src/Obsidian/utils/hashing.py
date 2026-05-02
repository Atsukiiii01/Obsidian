import hashlib


def sha256_file(path):
    hasher = hashlib.sha256()

    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            hasher.update(chunk)

    return hasher.hexdigest()
