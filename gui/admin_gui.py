import sys
from pathlib import Path

# --- FIX IMPORT PATH ---
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
# ----------------------

import tkinter as tk
from tkinter import filedialog, messagebox

from core.engine import identify_file
from core.learner import learn_signature

# ----------------------
# CYBER THEME CONSTANTS
# ----------------------
BG_MAIN = "#0b0f14"
BG_PANEL = "#111827"
FG_TEXT = "#e5e7eb"
FG_ACCENT = "#22c55e"
FG_WARN = "#facc15"

FONT_TITLE = ("Consolas", 14, "bold")
FONT_BODY = ("Consolas", 10)
FONT_BUTTON = ("Consolas", 10, "bold")

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OBSIDIAN — Admin Learning Console")
        self.root.geometry("560x420")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        self.file_path = None
        self.file_bytes = None

        self.build_ui()

    def build_ui(self):
        # ---------- HEADER ----------
        header = tk.Frame(self.root, bg=BG_MAIN)
        header.pack(fill="x", pady=(12, 6))

        tk.Label(
            header,
            text="OBSIDIAN",
            fg=FG_ACCENT,
            bg=BG_MAIN,
            font=FONT_TITLE
        ).pack()

        tk.Label(
            header,
            text="Admin Learning • Signature Correction",
            fg=FG_TEXT,
            bg=BG_MAIN,
            font=FONT_BODY
        ).pack(pady=(2, 8))

        # ---------- CONTROL PANEL ----------
        panel = tk.Frame(self.root, bg=BG_PANEL)
        panel.pack(fill="x", padx=12, pady=6)

        tk.Button(
            panel,
            text="SELECT FILE",
            command=self.select_file,
            bg=BG_MAIN,
            fg=FG_ACCENT,
            font=FONT_BUTTON,
            relief="flat",
            padx=14,
            pady=6
        ).pack(side="left", padx=8)

        self.status = tk.Label(
            panel,
            text="STANDBY",
            fg=FG_WARN,
            bg=BG_PANEL,
            font=FONT_BODY
        )
        self.status.pack(side="right", padx=10)

        # ---------- OUTPUT ----------
        self.output = tk.Text(
            self.root,
            height=10,
            bg=BG_MAIN,
            fg=FG_TEXT,
            insertbackground=FG_ACCENT,
            font=FONT_BODY,
            wrap="none",
            relief="flat"
        )
        self.output.pack(fill="x", padx=12, pady=(6, 4))

        # ---------- LEARN PANEL ----------
        learn_panel = tk.Frame(self.root, bg=BG_PANEL)
        learn_panel.pack(fill="x", padx=12, pady=6)

        tk.Label(
            learn_panel,
            text="Correct Type:",
            fg=FG_TEXT,
            bg=BG_PANEL,
            font=FONT_BODY
        ).pack(side="left", padx=6)

        self.correct_type = tk.Entry(
            learn_panel,
            width=16,
            bg=BG_MAIN,
            fg=FG_ACCENT,
            insertbackground=FG_ACCENT,
            relief="flat",
            font=FONT_BODY
        )
        self.correct_type.pack(side="left", padx=6)

        tk.Button(
            learn_panel,
            text="LEARN SIGNATURE",
            command=self.learn,
            bg=BG_MAIN,
            fg=FG_ACCENT,
            font=FONT_BUTTON,
            relief="flat",
            padx=14,
            pady=6
        ).pack(side="right", padx=10)

    def log(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    def select_file(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        self.file_path = Path(path).resolve()
        result, data = identify_file(str(self.file_path), return_bytes=True)
        self.file_bytes = data

        self.status.config(text="ANALYZED")

        output = (
            f"File: {self.file_path}\n\n"
            f"Detected Type: {result['type']}\n"
            f"Entropy: {result['entropy']}\n"
            f"Confidence: {result['confidence']}\n"
        )

        if result.get("hints"):
            output += "\nIntegrity Hints:\n"
            for h in result["hints"]:
                output += f"  ⚠ {h}\n"

        self.log(output)

    def learn(self):
        if not self.file_path or not self.file_bytes:
            messagebox.showerror("Error", "No file selected")
            return

        correct = self.correct_type.get().strip().upper()
        if not correct:
            messagebox.showerror("Error", "Enter correct file type")
            return

        learned = learn_signature(
            file_path=str(self.file_path),
            file_bytes=self.file_bytes,
            correct_type=correct,
            offset=0,
            length=8
        )

        if learned:
            self.status.config(text="LEARNED")
            messagebox.showinfo(
                "Success",
                f"Signature learned for {correct}"
            )
        else:
            messagebox.showwarning(
                "Info",
                "Signature already exists"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()
