from core.signatures import match_signatures
from core.heuristics import is_probably_text
from core.entropy import shannon_entropy
from core.corruption import corruption_hints
from utils.file_reader import read_file_bytes

def identify_file(path: str, return_bytes: bool = False):
    data = read_file_bytes(path)
    entropy = shannon_entropy(data)

    signature_hits = match_signatures(data)
    is_text = is_probably_text(data)

    result = {
        "file": path,
        "type": "UNKNOWN",
        "entropy": round(entropy, 3),
        "confidence": 0.0,
        "hints": []
    }

    if signature_hits:
        best = max(signature_hits, key=lambda x: x[1])
        result["type"] = best[0]
        result["confidence"] = best[1]

    elif is_text:
        result["type"] = "TEXT"
        result["confidence"] = 0.85

    elif entropy > 7.5:
        result["type"] = "BINARY/COMPRESSED"
        result["confidence"] = 0.6

    else:
        result["type"] = "BINARY"
        result["confidence"] = 0.5

    # --- CORRUPTION HINTS ---
    result["hints"] = corruption_hints(
        path,
        result["type"],
        data,
        entropy
    )

    if return_bytes:
        return result, data

    return result
