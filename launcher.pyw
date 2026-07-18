import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog


def run_command(cmd, shell=True):
    log(f">>> {' '.join(cmd) if isinstance(cmd, list) else cmd}\n")
    process = subprocess.Popen(
        cmd,
        shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=os.getcwd()
    )
    for line in process.stdout:
        log(line)
    process.stdout.close()
    process.wait()
    return process.returncode


def log(text):
    output_box.config(state=tk.NORMAL)
    output_box.insert(tk.END, text)
    output_box.see(tk.END)
    output_box.config(state=tk.DISABLED)


def start_bot():
    def task():
        set_status("Бот запускается...")
        run_command("start.bat")
        set_status("Готов")
    threading.Thread(target=task, daemon=True).start()


def check_updates():
    def task():
        set_status("Проверка обновлений...")
        run_command("python updater.py")
        set_status("Готов")
    threading.Thread(target=task, daemon=True).start()


def push_github():
    def task():
        set_status("Пуш на GitHub...")
        msg = simpledialog.askstring("Commit", "Введите сообщение коммита:", initialvalue="Auto update")
        if not msg:
            set_status("Готов")
            return
        run_command(f'git add -A && git commit -m "{msg}" && git push origin main')
        set_status("Готов")
    threading.Thread(target=task, daemon=True).start()


def create_release():
    def task():
        set_status("Создание релиза...")
        run_command("python create_release.py")
        set_status("Готов")
    threading.Thread(target=task, daemon=True).start()


def open_folder():
    subprocess.Popen(f'explorer "{os.getcwd()}"')


def set_status(text):
    status_var.set(text)
    root.update_idletasks()


root = tk.Tk()
root.title("Playerok Auto Placement v2.0")
root.geometry("900x600")
root.configure(bg="#1e1e1e")
root.minsize(700, 450)

try:
    root.iconbitmap("icon.ico")
except:
    pass

font_header = ("Segoe UI", 20, "bold")
font_button = ("Segoe UI", 11, "bold")
font_log = ("Consolas", 10)
font_status = ("Segoe UI", 10)

color_bg = "#1e1e1e"
color_frame = "#252526"
color_accent = "#007acc"
color_text = "#ffffff"
color_log = "#d4d4d4"

header = tk.Label(
    root,
    text="Playerok Auto Placement",
    font=font_header,
    fg=color_accent,
    bg=color_bg
)
header.pack(pady=(20, 5))

sub_header = tk.Label(
    root,
    text="Universal Launcher",
    font=("Segoe UI", 12),
    fg="#aaaaaa",
    bg=color_bg
)
sub_header.pack(pady=(0, 20))

button_frame = tk.Frame(root, bg=color_bg)
button_frame.pack(pady=10)

buttons = [
    ("Запустить бота", start_bot, "#28a745"),
    ("Проверить обновления", check_updates, color_accent),
    ("Пуш на GitHub", push_github, "#6f42c1"),
    ("Создать релиз", create_release, "#fd7e14"),
    ("Открыть папку", open_folder, "#6c757d"),
]

for text, command, color in buttons:
    btn = tk.Button(
        button_frame,
        text=text,
        command=command,
        font=font_button,
        fg=color_text,
        bg=color,
        activebackground="#ffffff",
        activeforeground=color,
        width=18,
        height=2,
        bd=0,
        cursor="hand2"
    )
    btn.pack(side=tk.LEFT, padx=8, pady=5)

log_frame = tk.Frame(root, bg=color_frame, bd=2, relief=tk.SUNKEN)
log_frame.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)

output_box = scrolledtext.ScrolledText(
    log_frame,
    font=font_log,
    bg=color_frame,
    fg=color_log,
    insertbackground=color_text,
    state=tk.DISABLED,
    wrap=tk.WORD,
    bd=0,
    padx=10,
    pady=10
)
output_box.pack(fill=tk.BOTH, expand=True)

status_var = tk.StringVar(value="Готов")
status_bar = tk.Label(
    root,
    textvariable=status_var,
    font=font_status,
    fg="#aaaaaa",
    bg=color_bg,
    anchor=tk.W
)
status_bar.pack(fill=tk.X, padx=20, pady=(0, 10))

log("Playerok Auto Placement Launcher запущен.\n")
log("Нажмите кнопку, чтобы начать.\n")

root.mainloop()
