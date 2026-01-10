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

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/obsidian.git
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