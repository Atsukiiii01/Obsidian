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

## 📂 Project Structure

```text
gui/        → Cyber GUIs (Launcher, Admin, Batch, Advanced)
core/       → Detection, heuristics, learning logic
database/   → SQLite knowledge base
utils/      → Helpers (export, hashing, IO)