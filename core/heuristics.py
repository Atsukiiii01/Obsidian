from core.entropy import shannon_entropy


def is_probably_text(data):
    if not data:
        return False

    if b"\x00" in data:
        return False

    printable = sum(
        1
        for byte in data
        if 32 <= byte <= 126 or byte in b"\n\r\t"
    )

    ratio = printable / len(data)
    entropy = shannon_entropy(data)

    return ratio > 0.90 and entropy < 5.5
