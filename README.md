# OBSIDIAN — Cyber File Analysis Console

OBSIDIAN is a **cyber-themed, self-learning file identification engine**

It combines:
- Magic signature detection
- Heuristic analysis
- Entropy inspection
- SQLite-backed learning
- Dark cyber GUI + console launcher

This project is designed to feel like a **forensics / SOC / recovery tool**.

---

## Features

- Single-file analysis (Admin mode)
- Batch folder scanning
- Self-learning signature engine
- SQLite knowledge base
- Corruption & integrity hints
- CSV / JSON export
- Cross-platform (macOS / Windows)

---

## ---How to Run---

```bash

### 1. Clone Repo..

git clone https://github.com/Atsukiiii01/obsidian.git
cd obsidian

### 2. Create virtual environment

python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows

### 3. Initialize database
python database/init_db.py

### 4. Launch OBSIDIAN
python gui/launcher.py

### ----Project Structure----
gui/        → Cyber GUIs (Launcher, Admin, Batch, Advanced)
core/       → Detection, heuristics, learning logic
database/   → SQLite knowledge base
utils/      → Helpers (export, hashing, IO)

### Disclaimer ###

This tool provides analysis and hints, not guarantees.
It does NOT modify files.
# ⬢ Obsidian | Static Forensic Analysis Engine

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux-lightgrey.svg)

**Obsidian** is a lightweight, zero-dependency static analysis engine designed for rapid triage of suspicious files, malware, and obfuscated payloads. 

Unlike traditional static identifiers that rely solely on file headers, Obsidian uses a bi-directional scanning architecture (Headers & Footers), mathematical entropy calculation, and raw byte-level string extraction to expose a file's true capabilities.

## ⚡ Core Capabilities

* **Bi-Directional Signature Matching:** Scans both `[0:8192]` and `[-512:]` offsets to catch heavily packed, appended, or maliciously structured files (e.g., Apple UDIF `koly` blocks).
* **Cryptographic Identity:** Automatically generates `MD5`, `SHA-1`, and `SHA-256` hashes via memory-safe chunking for immediate IOC threat intelligence lookups.
* **Heuristic Anomaly Detection:** Compares mathematical Shannon Entropy against identified signatures to flag zero-padding, sparse data, or heavy obfuscation.
* **Artifact Extraction:** Strips binaries to extract embedded IPv4 Command and Control (C2) servers, URLs, and Cryptocurrency Wallets using strict `ipaddress` validation to eliminate false positives.
* **Zero-Dependency:** Operates entirely on the Python Standard Library. No external packages required. 

## 🛠 Installation & Setup

Obsidian is built for rapid deployment. Clone the repository and seed the intelligence vault:
```bash
git clone https://github.com/Atsukiiii01/Obsidian.git
cd Obsidian
python3 setup_db.py

Global Execution (macOS / Linux)
To run Obsidian seamlessly from anywhere in your terminal:

Bash
chmod +x obsidian.py
echo 'alias obsidian="/path/to/Obsidian/obsidian.py"' >> ~/.zshrc
source ~/.zshrc

*Usage*
Run Obsidian against a single target or an entire directory for bulk triage.

Bash
# Analyze a single payload
obsidian /path/to/suspicious_file.bin

# Output raw JSON for pipeline integration
obsidian /path/to/suspicious_file.bin --json

(Architectural Note)
Obsidian was engineered to solve the specific problem of "silent failures" in standard magic byte scanners. By incorporating negative-offset signature matching and structural heuristics, it acts as an X-ray for analysts before detonating payloads in a sandbox environment.