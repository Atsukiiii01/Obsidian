import sys
from pathlib import Path
import subprocess
import tkinter as tk


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


BG = "#05080d"
FG = "#22c55e"
FG_DIM = "#94a3b8"
FG_WARN = "#facc15"

FONT_TITLE = ("Consolas", 18, "bold")
FONT_MENU = ("Consolas", 14)
FONT_BOOT = ("Consolas", 11)
FONT_HINT = ("Consolas", 9)

MENU_OPTIONS = [
    ("SINGLE FILE ANALYZER", "admin_gui.py"),
    ("BATCH SCAN MODULE", "batch_scan_gui.py"),
    ("ADVANCED CONSOLE", "advanced_gui.py"),
]

BOOT_SEQUENCE = [
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

        self.selected = 0
        self.cursor_on = True
        self.boot_step = 0

        self.setup_boot()
        self.run_boot()

    def setup_boot(self):
        self.boot_container = tk.Frame(self.root, bg=BG)
        self.boot_container.pack(fill="both", expand=True)

        self.boot_output = tk.Text(
            self.boot_container,
            bg=BG,
            fg=FG,
            font=FONT_BOOT,
            relief="flat",
            wrap="none",
            state="disabled"
        )
        self.boot_output.pack(fill="both", expand=True, padx=20, pady=20)

    def run_boot(self):
        if self.boot_step < len(BOOT_SEQUENCE):
            self.append_boot_line(BOOT_SEQUENCE[self.boot_step])
            self.boot_step += 1
            self.root.after(600, self.run_boot)
        else:
            self.root.after(700, self.show_menu)

    def append_boot_line(self, text):
        self.boot_output.config(state="normal")
        self.boot_output.insert(tk.END, text + "\n")
        self.boot_output.see(tk.END)
        self.boot_output.config(state="disabled")

    def show_menu(self):
        self.boot_container.destroy()

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

        self.menu_container = tk.Frame(self.root, bg=BG)
        self.menu_container.pack()

        self.menu_labels = []
        for label, _ in MENU_OPTIONS:
            item = tk.Label(
                self.menu_container,
                text=label,
                fg=FG_DIM,
                bg=BG,
                font=FONT_MENU,
                anchor="w",
                width=30
            )
            item.pack(pady=6)
            self.menu_labels.append(item)

        self.update_selection()

        tk.Label(
            self.root,
            text="↑ ↓ Navigate    ENTER Execute    ESC Exit",
            fg=FG_DIM,
            bg=BG,
            font=FONT_HINT
        ).pack(side="bottom", pady=15)

        self.bind_keys()
        self.blink_cursor()

    def update_selection(self):
        for i, label in enumerate(self.menu_labels):
            if i == self.selected:
                prefix = "▶ " if self.cursor_on else "  "
                label.config(text=prefix + MENU_OPTIONS[i][0], fg=FG)
            else:
                label.config(text="  " + MENU_OPTIONS[i][0], fg=FG_DIM)

    def blink_cursor(self):
        self.cursor_on = not self.cursor_on
        self.update_selection()
        self.root.after(500, self.blink_cursor)

    def bind_keys(self):
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Return>", self.launch_selected)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def move_up(self, event):
        self.selected = (self.selected - 1) % len(MENU_OPTIONS)
        self.update_selection()

    def move_down(self, event):
        self.selected = (self.selected + 1) % len(MENU_OPTIONS)
        self.update_selection()

    def launch_selected(self, event):
        script = MENU_OPTIONS[self.selected][1]
        subprocess.Popen(
            [sys.executable, str(Path(__file__).parent / script)],
            cwd=BASE_DIR
        )


if __name__ == "__main__":
    root = tk.Tk()
    ConsoleLauncher(root)
    root.mainloop()
