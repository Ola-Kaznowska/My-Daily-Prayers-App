import tkinter as tk
from tkinter import ttk, messagebox

# =====================
# CONFIGURATION
# =====================
PASSWORD = "islam123"

PRAYERS = [
    {
        "name": "Fajr",
        "time": "Morning (before sunrise)",
        "desc": "The morning prayer, performed before sunrise.",
        "done": False
    },
    {
        "name": "Dhuhr",
        "time": "Midday",
        "desc": "The noon prayer, performed after the sun passes its zenith.",
        "done": False
    },
    {
        "name": "Asr",
        "time": "Afternoon",
        "desc": "The afternoon prayer, performed in the late part of the day.",
        "done": False
    },
    {
        "name": "Maghrib",
        "time": "Evening (after sunset)",
        "desc": "The evening prayer, performed just after sunset.",
        "done": False
    },
    {
        "name": "Isha",
        "time": "Night",
        "desc": "The night prayer, performed after darkness falls.",
        "done": False
    },
]


DARK = {
    "bg": "#1e1e1e",
    "fg": "#eaeaea",
    "accent": "#2d8cff",
    "success": "#3cb371"
}

LIGHT = {
    "bg": "#f4f4f4",
    "fg": "#111111",
    "accent": "#2d8cff",
    "success": "#228b22"
}



class PrayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Prayer Reminder")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.theme = DARK
        self.login_screen()

    
    def login_screen(self):
        self.clear()
        self.apply_theme()

        tk.Label(
            self.root,
            text="Daily Prayer Reminder",
            font=("Segoe UI", 24, "bold"),
            bg=self.theme["bg"],
            fg=self.theme["accent"]
        ).pack(pady=40)

        tk.Label(
            self.root,
            text="Enter password",
            font=("Segoe UI", 14),
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        ).pack(pady=10)

        self.password_entry = tk.Entry(
            self.root,
            show="*",
            font=("Segoe UI", 14),
            width=22,
            bg="#2b2b2b",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.password_entry.pack(pady=10)
        self.password_entry.focus()

        tk.Button(
            self.root,
            text="Login",
            font=("Segoe UI", 14, "bold"),
            bg=self.theme["accent"],
            fg="white",
            width=16,
            relief="flat",
            command=self.start_login
        ).pack(pady=20)

        self.progress = ttk.Progressbar(self.root, length=320, mode="determinate")

    def start_login(self):
        self.progress.pack(pady=10)
        self.progress["value"] = 0
        self.animate_login()

    def animate_login(self):
        if self.progress["value"] < 100:
            self.progress["value"] += 10
            self.root.after(40, self.animate_login)
        else:
            self.check_password()

    def check_password(self):
        if self.password_entry.get() == PASSWORD:
            self.main_screen()
        else:
            self.progress.pack_forget()
            self.progress["value"] = 0
            messagebox.showerror("Error", "Incorrect password")

    
    def main_screen(self):
        self.clear()
        self.apply_theme()

        top = tk.Frame(self.root, bg=self.theme["bg"])
        top.pack(pady=10)

        tk.Label(
            top,
            text="Your Daily Prayers",
            font=("Segoe UI", 20, "bold"),
            bg=self.theme["bg"],
            fg=self.theme["accent"]
        ).pack(side="left", padx=10)

        tk.Button(
            top,
            text="Toggle theme",
            font=("Segoe UI", 10),
            bg="#555",
            fg="white",
            relief="flat",
            command=self.toggle_theme
        ).pack(side="right")

        self.progress_label = tk.Label(
            self.root,
            font=("Segoe UI", 14),
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        )
        self.progress_label.pack(pady=10)

        self.prayer_vars = []

        for i, prayer in enumerate(PRAYERS):
            var = tk.BooleanVar(value=prayer["done"])

            cb = tk.Checkbutton(
                self.root,
                text=f"{prayer['name']} — {prayer['time']}",
                font=("Segoe UI", 14),
                variable=var,
                bg=self.theme["bg"],
                fg=self.theme["fg"],
                selectcolor=self.theme["bg"],
                activebackground=self.theme["bg"],
                activeforeground=self.theme["success"],
                command=self.update_prayers
            )
            cb.pack(anchor="w", padx=50, pady=6)

            info = tk.Button(
                self.root,
                text="?",
                font=("Segoe UI", 10, "bold"),
                width=2,
                bg=self.theme["accent"],
                fg="white",
                relief="flat",
                command=lambda p=prayer: self.show_info(p)
            )
            info.pack(anchor="w", padx=70)

            self.prayer_vars.append(var)

        tk.Button(
            self.root,
            text="Reset prayers",
            font=("Segoe UI", 12, "bold"),
            bg="#444",
            fg=self.theme["fg"],
            width=18,
            relief="flat",
            command=self.reset_prayers
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Exit",
            font=("Segoe UI", 12, "bold"),
            bg="#aa3333",
            fg="white",
            width=18,
            relief="flat",
            command=self.root.quit
        ).pack()

        self.update_progress_text()

    
    def update_prayers(self):
        for i, var in enumerate(self.prayer_vars):
            PRAYERS[i]["done"] = var.get()
        self.update_progress_text()

    def update_progress_text(self):
        completed = sum(1 for p in PRAYERS if p["done"])
        self.progress_label.config(text=f"Completed today: {completed} / {len(PRAYERS)}")

    def reset_prayers(self):
        for i, var in enumerate(self.prayer_vars):
            var.set(False)
            PRAYERS[i]["done"] = False
        self.update_progress_text()

    def show_info(self, prayer):
        messagebox.showinfo(prayer["name"], prayer["desc"])

    
    def toggle_theme(self):
        self.theme = LIGHT if self.theme == DARK else DARK
        self.main_screen()

    def apply_theme(self):
        self.root.configure(bg=self.theme["bg"])

    
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()




if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("default")
    PrayerApp(root)
    root.mainloop()