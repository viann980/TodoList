import tkinter as tk
import customtkinter as ctk
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("todo_expert.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                   (id INTEGER PRIMARY KEY, task TEXT, priority TEXT, status INTEGER)''')
    conn.commit()
    conn.close()

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ZenList - Daily Task Manager")
        self.geometry("500x600")
        ctk.set_appearance_mode("dark")
        
        init_db()

        # Layout Grid
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        self.label = ctk.CTkLabel(self, text="Rencana Hari Ini", font=("Helvetica", 24, "bold"))
        self.label.pack(pady=20)

        # Input Frame
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.task_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Apa yang ingin dikerjakan?", width=250)
        self.task_entry.pack(side="left", padx=10, pady=10)

        self.priority_option = ctk.CTkOptionMenu(self.input_frame, values=["Tinggi", "Sedang", "Rendah"], width=100)
        self.priority_option.pack(side="left", padx=5)

        self.add_button = ctk.CTkButton(self.input_frame, text="+", width=40, command=self.add_task)
        self.add_button.pack(side="left", padx=5)

        # Scrollable Frame for Tasks
        self.tasks_frame = ctk.CTkScrollableFrame(self, label_text="Daftar Tugas", width=450, height=350)
        self.tasks_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_option.get()
        if task:
            conn = sqlite3.connect("todo_expert.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task, priority, status) VALUES (?, ?, ?)", (task, priority, 0))
            conn.commit()
            conn.close()
            self.task_entry.delete(0, 'end')
            self.load_tasks()

    def load_tasks(self):
        # Bersihkan frame sebelum load ulang
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("todo_expert.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks ORDER BY status ASC, id DESC")
        rows = cursor.fetchall()

        for row in rows:
            self.render_task_row(row)
        conn.close()

    def render_task_row(self, row):
        task_id, task_text, priority, status = row
        
        color = "#ff4d4d" if priority == "Tinggi" else "#ffa500" if priority == "Sedang" else "#4da6ff"
        
        row_frame = ctk.CTkFrame(self.tasks_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=5)

        # Checkbox untuk status
        check_var = tk.BooleanVar(value=True if status == 1 else False)
        cb = ctk.CTkCheckBox(row_frame, text=f"[{priority}] {task_text}", 
                             variable=check_var, command=lambda: self.toggle_task(task_id, check_var.get()),
                             border_color=color, text_color="white" if status == 0 else "gray")
        cb.pack(side="left", padx=10)

        # Tombol Hapus
        del_btn = ctk.CTkButton(row_frame, text="Hapus", width=60, height=25, fg_color="#333333", hover_color="#cc0000",
                                command=lambda: self.delete_task(task_id))
        del_btn.pack(side="right", padx=10)

    def toggle_task(self, task_id, is_done):
        status = 1 if is_done else 0
        conn = sqlite3.connect("todo_expert.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
        conn.commit()
        conn.close()
        self.load_tasks()

    def delete_task(self, task_id):
        conn = sqlite3.connect("todo_expert.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        self.load_tasks()

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()