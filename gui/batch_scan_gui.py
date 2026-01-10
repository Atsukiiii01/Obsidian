import sys
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.engine import identify_file
from utils.exporter import export_csv, export_json


BG_MAIN = "#0b0f14"
BG_PANEL = "#111827"
FG_TEXT = "#e5e7eb"
FG_ACCENT = "#22c55e"
FG_WARN = "#facc15"

FONT_TITLE = ("Consolas", 14, "bold")
FONT_BODY = ("Consolas", 10)
FONT_BUTTON = ("Consolas", 10, "bold")


class BatchScanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OBSIDIAN — File Analysis Engine")
        self.root.geometry("820x480")
        self.root.configure(bg=BG_MAIN)

        self.results = []
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg=BG_MAIN)
        header.pack(fill="x", pady=(10, 5))

        tk.Label(
            header,
            text="OBSIDIAN",
            fg=FG_ACCENT,
            bg=BG_MAIN,
            font=FONT_TITLE
        ).pack()

        tk.Label(
            header,
            text="Signature Analysis • Integrity Hints • Deep Scan",
            fg=FG_TEXT,
            bg=BG_MAIN,
            font=FONT_BODY
        ).pack(pady=(2, 6))

        panel = tk.Frame(self.root, bg=BG_PANEL)
        panel.pack(fill="x", padx=10, pady=6)

        tk.Button(
            panel,
            text="SELECT FOLDER",
            command=self.select_folder,
            bg=BG_MAIN,
            fg=FG_ACCENT,
            font=FONT_BUTTON,
            relief="flat",
            padx=12,
            pady=6
        ).pack(side="left", padx=6)

        tk.Button(
            panel,
            text="EXPORT CSV",
            command=self.save_csv,
            bg=BG_MAIN,
            fg=FG_ACCENT,
            font=FONT_BUTTON,
            relief="flat",
            padx=12,
            pady=6
        ).pack(side="left", padx=6)

        tk.Button(
            panel,
            text="EXPORT JSON",
            command=self.save_json,
            bg=BG_MAIN,
            fg=FG_ACCENT,
            font=FONT_BUTTON,
            relief="flat",
            padx=12,
            pady=6
        ).pack(side="left", padx=6)

        self.status = tk.Label(
            panel,
            text="STANDBY",
            fg=FG_WARN,
            bg=BG_PANEL,
            font=FONT_BODY
        )
        self.status.pack(side="right", padx=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Cyber.Horizontal.TProgressbar",
            troughcolor=BG_PANEL,
            background=FG_ACCENT,
            thickness=8
        )

        self.progress = ttk.Progressbar(
            self.root,
            style="Cyber.Horizontal.TProgressbar",
            orient="horizontal",
            mode="determinate"
        )
        self.progress.pack(fill="x", padx=12, pady=(6, 4))

        self.output = tk.Text(
            self.root,
            bg=BG_MAIN,
            fg=FG_TEXT,
            insertbackground=FG_ACCENT,
            font=FONT_BODY,
            wrap="none",
            relief="flat"
        )
        self.output.pack(fill="both", expand=True, padx=12, pady=(4, 10))

    def write_line(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.output.delete("1.0", tk.END)
        self.results.clear()
        self.status.config(text="SCANNING")
        self.progress["value"] = 0

        threading.Thread(
            target=self.scan_folder,
            args=(Path(folder),),
            daemon=True
        ).start()

    def scan_folder(self, folder: Path):
        files = [p for p in folder.rglob("*") if p.is_file()]
        total = len(files)

        if total == 0:
            self.status.config(text="NO FILES")
            return

        self.progress["maximum"] = total

        for index, file in enumerate(files, start=1):
            try:
                analysis = identify_file(str(file))
                entry = {
                    "file": str(file),
                    "type": analysis["type"],
                    "entropy": analysis["entropy"],
                    "confidence": analysis["confidence"]
                }
                self.results.append(entry)

                self.write_line(
                    f"[{index}/{total}] "
                    f"{file.name} | "
                    f"{entry['type']} | "
                    f"entropy={entry['entropy']} | "
                    f"conf={entry['confidence']}"
                )

                if analysis.get("hints"):
                    for hint in analysis["hints"]:
                        self.write_line(f"   ⚠ {hint}")

            except Exception as err:
                self.write_line(f"{file} | ERROR: {err}")

            self.progress["value"] = index
            self.status.config(text=f"{index}/{total}")

        self.status.config(text="COMPLETED")

    def save_csv(self):
        if not self.results:
            messagebox.showwarning("No Data", "No scan results to export")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )

        if path:
            export_csv(self.results, Path(path))
            messagebox.showinfo("Exported", "CSV export completed")

    def save_json(self):
        if not self.results:
            messagebox.showwarning("No Data", "No scan results to export")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )

        if path:
            export_json(self.results, Path(path))
            messagebox.showinfo("Exported", "JSON export completed")


if __name__ == "__main__":
    root = tk.Tk()
    BatchScanGUI(root)
    root.mainloop()
