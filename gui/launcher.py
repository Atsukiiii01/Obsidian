import sys
from pathlib import Path

# --- import fix ---
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
# ------------------

import tkinter as tk
import subprocess

# -------- THEME --------
BG = "#05080d"
FG = "#22c55e"
FG_DIM = "#94a3b8"
FG_WARN = "#facc15"

FONT_TITLE = ("Consolas", 18, "bold")
FONT_MENU = ("Consolas", 14)
FONT_BOOT = ("Consolas", 11)
FONT_HINT = ("Consolas", 9)

OPTIONS = [
    ("SINGLE FILE ANALYZER", "admin_gui.py"),
    ("BATCH SCAN MODULE", "batch_scan_gui.py"),
    ("ADVANCED CONSOLE", "advanced_gui.py"),
]

BOOT_LINES = [
    "[BOOT] Initializing OBSIDIAN Core...",
    "[ OK ] Signature Engine Loaded",
    "[ OK ] SQLite Knowledge Base Connected",
    "[ OK ] Heuristic Analyzer Online",
    "[ OK ] Learning Module Armed",
    "[SYS] SYSTEM ONLINE",
]

class ConsoleLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("OBSIDIAN // CONSOLE")
        self.root.geometry("640x420")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.index = 0
        self.cursor_visible = True
        self.boot_index = 0

        self.build_boot_ui()
        self.play_boot_sequence()

    # ---------- BOOT UI ----------
    def build_boot_ui(self):
        self.boot_frame = tk.Frame(self.root, bg=BG)
        self.boot_frame.pack(fill="both", expand=True)

        self.boot_text = tk.Text(
            self.boot_frame,
            bg=BG,
            fg=FG,
            font=FONT_BOOT,
            relief="flat",
            wrap="none",
            state="disabled"
        )
        self.boot_text.pack(fill="both", expand=True, padx=20, pady=20)

    def play_boot_sequence(self):
        if self.boot_index < len(BOOT_LINES):
            self.write_line(BOOT_LINES[self.boot_index])
            self.boot_index += 1
            self.root.after(600, self.play_boot_sequence)
        else:
            self.root.after(700, self.show_menu)

    def write_line(self, line):
        self.boot_text.config(state="normal")
        self.boot_text.insert(tk.END, line + "\n")
        self.boot_text.see(tk.END)
        self.boot_text.config(state="disabled")

    # ---------- MAIN MENU ----------
    def show_menu(self):
        self.boot_frame.destroy()
        self.build_menu_ui()
        self.animate_cursor()
        self.bind_keys()

    def build_menu_ui(self):
        # Header
        tk.Label(
            self.root,
            text="OBSIDIAN",
            fg=FG,
            bg=BG,
            font=FONT_TITLE
        ).pack(pady=(20, 5))

        self.status = tk.Label(
            self.root,
            text="SYSTEM ONLINE // STANDBY",
            fg=FG_WARN,
            bg=BG,
            font=FONT_HINT
        )
        self.status.pack(pady=(0, 20))

        # Menu
        self.menu_frame = tk.Frame(self.root, bg=BG)
        self.menu_frame.pack()

        self.menu_labels = []
        for text, _ in OPTIONS:
            lbl = tk.Label(
                self.menu_frame,
                text=text,
                fg=FG_DIM,
                bg=BG,
                font=FONT_MENU,
                anchor="w",
                width=30
            )
            lbl.pack(pady=6)
            self.menu_labels.append(lbl)

        self.update_menu()

        # Footer
        tk.Label(
            self.root,
            text="↑ ↓ Navigate    ENTER Execute    ESC Exit",
            fg=FG_DIM,
            bg=BG,
            font=FONT_HINT
        ).pack(side="bottom", pady=15)

    def update_menu(self):
        for i, lbl in enumerate(self.menu_labels):
            if i == self.index:
                cursor = "▶ " if self.cursor_visible else "  "
                lbl.config(text=cursor + OPTIONS[i][0], fg=FG)
            else:
                lbl.config(text="  " + OPTIONS[i][0], fg=FG_DIM)

    def animate_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.update_menu()
        self.root.after(500, self.animate_cursor)

    def bind_keys(self):
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Return>", self.execute)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def move_up(self, event):
        self.index = (self.index - 1) % len(OPTIONS)
        self.update_menu()

    def move_down(self, event):
        self.index = (self.index + 1) % len(OPTIONS)
        self.update_menu()

    def execute(self, event):
        script = OPTIONS[self.index][1]
        subprocess.Popen(
            [sys.executable, str(Path(__file__).parent / script)],
            cwd=BASE_DIR
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = ConsoleLauncher(root)
    root.mainloop()

