from pathlib import Path

def generate_hints(file_path, file_type, entropy, confidence):
    hints = []
    ext = Path(file_path).suffix.lower()
    
    # 1. Container Anomalies
    if any(container in file_type for container in ["UDIF", "ZIP", "Zlib"]):
        if entropy < 7.0:
            hints.append("Anomaly: Low entropy for a compressed container. Suggests zero-padding, sparse data, or uncompressed payloads.")
            
    # 2. Text Anomalies
    if file_type == "TEXT":
        if entropy > 6.0:
            hints.append("Anomaly: High entropy for text. Check for Base64 encoded payloads or heavy obfuscation.")
            
    # 3. Confidence Warnings
    if confidence < 0.8 and file_type != "BINARY":
        hints.append("Warning: Low confidence signature match. File may be corrupted or intentionally malformed.")

    # 4. Extension Spoofing (The Threat Hunter Rule)
    executables = ["Mach-O", "ELF Binary", "EXECUTABLE (MZ)"]
    safe_executable_exts = ['.exe', '.dll', '.app', '.bin', '.elf', '.macho', '.run']
    
    if any(exe in file_type for exe in executables):
        if ext and ext not in safe_executable_exts:
            hints.append(f"CRITICAL: Extension mismatch. File claims to be '{ext}' but signature indicates an executable binary.")

    return hints