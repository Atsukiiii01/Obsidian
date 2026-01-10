from core.signatures import match_signatures
from core.heuristics import is_probably_text
from core.entropy import shannon_entropy
from core.corruption import corruption_hints
from utils.file_reader import read_file_bytes


def identify_file(path, return_bytes=False):
    raw_bytes = read_file_bytes(path)
    entropy = shannon_entropy(raw_bytes)

    matches = match_signatures(raw_bytes)
    looks_text = is_probably_text(raw_bytes)

    analysis = {
        "file": path,
        "type": "UNKNOWN",
        "entropy": round(entropy, 3),
        "confidence": 0.0,
        "hints": []
    }

    if matches:
        file_type, confidence = max(matches, key=lambda item: item[1])
        analysis["type"] = file_type
        analysis["confidence"] = confidence

    elif looks_text:
        analysis["type"] = "TEXT"
        analysis["confidence"] = 0.85

    elif entropy > 7.5:
        analysis["type"] = "BINARY/COMPRESSED"
        analysis["confidence"] = 0.6

    else:
        analysis["type"] = "BINARY"
        analysis["confidence"] = 0.5

    analysis["hints"] = corruption_hints(
        path,
        analysis["type"],
        raw_bytes,
        entropy
    )

    if return_bytes:
        return analysis, raw_bytes

    return analysis
