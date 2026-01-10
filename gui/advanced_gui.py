import sys
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.engine import identify_file
from core.learner import learn_signature


BG_MAIN = "#0b0f14"
BG_PANEL = "#111827"
FG_TEXT = "#e5e7eb"
FG_ACCENT = "#22c55e"
FG_WARN = "#facc15"

FONT_TITLE = ("Consolas", 14, "bold")
FONT_BODY = ("Consolas", 10)
FONT_BUTTON = ("Consolas", 10, "bold")


class ObsidianGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OBSIDIAN — Advanced File Analysis Console")
        self.root.geometry("900x520")
        self.root.configure(bg=BG_MAIN)

        self.results = []
        self.selected_row = None

        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg=BG_MAIN)
        header.pack(fill="x", pady=8)

        tk.Label(
            header,
            text="OBSIDIAN",
            fg=FG_ACCENT,
            bg=BG_MAIN,
            font=FONT_TITLE
        ).pack()

        tk.Label(
            header,
            text="Advanced File Analysis • Learning Engine • Integrity Hints",
            fg=FG_TEXT,
            bg=BG_MAIN,
            font=FONT_BODY
        ).pack()

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_scan_tab()
        self.build_results_tab()
        self.build_learn_tab()

    def build_scan_tab(self):
        tab = tk.Frame(self.tabs, bg=BG_PANEL)
        self.tabs.add(tab, text=" Scan ")

        tk.Button(
            tab,
            text="SELECT FOLDER & SCAN",
            command=self.select_folder,
            bg=BG_MAIN,
            fg=FG_ACCENT,
            font=FONT_BUTTON,
            relief="flat",
            padx=16,
            pady=8
        ).pack(pady=20)

        self.scan_status = tk.Label(
            tab,
            text="STANDBY",
            fg=FG_WARN,
            bg=BG_PANEL,
            font=FONT_BODY
        )
        self.scan_status.pack()

    def build_results_tab(self):
        tab = tk.Frame(self.tabs, bg=BG_PANEL)
        self.tabs.add(tab, text=" Results ")

        columns = ("file", "type", "entropy", "confidence")

        self.tree = ttk.Treeview(
            tab,
            columns=columns,
            show="headings",
            height=18
        )

        for col in columns:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def build_learn_tab(self):
        tab = tk.Frame(self.tabs, bg=BG_PANEL)
        self.tabs.add(tab, text=" Learn ")

        tk.Label(
            tab,
            text="Selected File:",
            fg=FG_TEXT,
            bg=BG_PANEL,
            font=FONT_BODY
        ).pack(pady=(20, 5))

        self.selected_label = tk.Label(
            tab,
            text="None",
            fg=FG_WARN,
            bg=BG_PANEL,
            font=FONT_BODY
        )
        self.selected_label.pack(pady=4)

        tk.Label(
            tab,
            text="Correct Type:",
            fg=FG_TEXT,
            bg=BG_PANEL,
            font=FONT_BODY
        ).pack(pady=(20, 4))

        self.correct_type = tk.Entry(
            tab,
            bg=BG_MAIN,
            fg=FG_ACCENT,
            insertbackground=FG_ACCENT,
            font=FONT_BODY,
            relief="flat",
            width=20
        )
        self.correct_type.pack()

        tk.Button(
            tab,
            text="LEARN SIGNATURE",
            command=self.learn_signature_for_file,
            bg=BG_MAIN,
            fg=FG_ACCENT,
            font=FONT_BUTTON,
            relief="flat",
            padx=16,
            pady=8
        ).pack(pady=20)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.tree.delete(*self.tree.get_children())
        self.results.clear()
        self.scan_status.config(text="SCANNING")

        threading.Thread(
            target=self.scan_folder,
            args=(Path(folder),),
            daemon=True
        ).start()

    def scan_folder(self, folder: Path):
        files = [p for p in folder.rglob("*") if p.is_file()]

        for file in files:
            analysis = identify_file(str(file))
            row = (
                str(file),
                analysis["type"],
                analysis["entropy"],
                analysis["confidence"]
            )
            self.results.append((file, analysis))
            self.tree.insert("", "end", values=row)

        self.scan_status.config(text="COMPLETED")
        self.tabs.select(1)

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0])["values"]
        self.selected_row = values
        self.selected_label.config(text=values[0])
        self.tabs.select(2)

    def learn_signature_for_file(self):
        if not self.selected_row:
            messagebox.showerror("Error", "No file selected")
            return

        correct = self.correct_type.get().strip().upper()
        if not correct:
            messagebox.showerror("Error", "Enter correct type")
            return

        file_path = self.selected_row[0]
        _, raw_bytes = identify_file(file_path, return_bytes=True)

        learn_signature(
            file_path=file_path,
            file_bytes=raw_bytes,
            correct_type=correct
        )

        messagebox.showinfo(
            "Learned",
            f"Signature learned for {correct}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    ObsidianGUI(root)
    root.mainloop()
