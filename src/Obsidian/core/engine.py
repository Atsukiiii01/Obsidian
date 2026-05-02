from Obsidian.core.entropy import shannon_entropy
from Obsidian.core.signatures import match_signatures
from Obsidian.utils.file_reader import read_file_segments, is_probably_text
from Obsidian.core.heuristics import generate_hints
from Obsidian.core.crypto import generate_hashes
from Obsidian.core.strings import find_iocs  # <-- NEW IMPORT

def identify_file(path):
    # 1. Acquisition
    header, footer = read_file_segments(path)
    if not header:
        return {"file": str(path), "type": "EMPTY", "confidence": 1.0}

    # 2. Forensic Analysis
    entropy = shannon_entropy(header)
    matches = match_signatures(header, footer)
    looks_text = is_probably_text(header)
    
    # Generate Identity and Extract Artifacts
    hashes = generate_hashes(path)
    extracted_iocs = find_iocs(path) # <-- EXECUTE THE HUNTER

    # 3. Output Structure
    analysis = {
        "file": str(path),
        "type": "UNKNOWN",
        "entropy": round(entropy, 3),
        "confidence": 0.0,
        "hashes": hashes,
        "iocs": extracted_iocs,  # <-- NEW DATA INJECTED
        "hints": []
    }

    # 4. Hierarchy Logic
    if matches:
        f_type, conf = max(matches, key=lambda x: x[1])
        analysis["type"] = f_type
        analysis["confidence"] = conf
    elif looks_text:
        analysis["type"] = "TEXT"
        analysis["confidence"] = 0.9
    elif entropy > 7.5:
        analysis["type"] = "BINARY (ENCRYPTED/COMPRESSED)"
        analysis["confidence"] = 0.6
    else:
        analysis["type"] = "BINARY"
        analysis["confidence"] = 0.4

    # 5. Inject Heuristic Intelligence
    analysis["hints"] = generate_hints(
        path, 
        analysis["type"], 
        analysis["entropy"], 
        analysis["confidence"]
    )

    return analysis