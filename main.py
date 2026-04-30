import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных паролей")
        self.root.geometry("600x500")

        # Настройки символов
        self.chars = {
            'digits': '0123456789',
            'lower': 'abcdefghijklmnopqrstuvwxyz',
            'upper': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'special': '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }

        self.history = self.load_history()

        self.setup_ui()
        self.update_history_table()

    def setup_ui(self):
        # Ползунок длины
        tk.Label(self.root, text="Длина пароля (4-50):").pack(pady=5)
        self.length_var = tk.IntVar(value=12)
        self.length_scale = tk.Scale(self.root, from_=4, to=50, orient=tk.HORIZONTAL,
                                     variable=self.length_var, length=300)
        self.length_scale.pack(pady=5)
        self.length_label = tk.Label(self.root, text="12")
        self.length_label.pack()
        self.length_scale.config(command=self.update_length_label)

        # Чекбоксы
        frame_chars = tk.Frame(self.root)
        frame_chars.pack(pady=10)
        self.vars = {}
        for char_type, symbols in self.chars.items():
            var = tk.BooleanVar(value=True)
            self.vars[char_type] = var
            cb = tk.Checkbutton(frame_chars, text={
                'digits': 'Цифры', 'lower': 'Строчные буквы',
                'upper': 'Заглавные буквы', 'special': 'Спецсимволы'
            }[char_type], variable=var)
            cb.pack(anchor=tk.W)

        # Кнопка генерации
        tk.Button(self.root, text="Генерировать", command=self.generate_password,
                  bg="lightgreen", font=("Arial", 12, "bold")).pack(pady=20)

        # Поле пароля
        self.password_var = tk.StringVar()
        tk.Label(self.root, text="Сгенерированный пароль:").pack()
        self.password_entry = tk.Entry(self.root, textvariable=self.password_var,
                                       font=("Courier", 14), width=50, state=tk.DISABLED)
        self.password_entry.pack(pady=5)
        tk.Button(self.root, text="Копировать", command=self.copy_password).pack()

        # Таблица истории
        tk.Label(self.root, text="История:").pack(pady=(20, 5))
        self.tree = ttk.Treeview(self.root, columns=("Дата", "Пароль", "Длина"), show="headings", height=8)
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Пароль", text="Пароль")
        self.tree.heading("Длина", text="Длина")
        self.tree.column("Дата", width=120)
        self.tree.column("Пароль", width=300)
        self.tree.column("Длина", width=80)
        self.tree.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))

    def get_char_pool(self):
        pool = ""
        selected_count = 0
        for char_type, var in self.vars.items():
            if var.get():
                pool += self.chars[char_type]
                selected_count += 1
        if selected_count == 0:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return ""
        if len(pool) == 0:
            return ""
        return pool

    def generate_password(self):
        length = self.length_var.get()
        pool = self.get_char_pool()
        if not pool:
            return
        password = ''.join(random.choice(pool) for _ in range(length))
        self.password_var.set(password)
        self.password_entry.config(state=tk.NORMAL)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.password_entry.config(state=tk.DISABLED)

        # Сохранить в историю
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "password": password,
            "length": length
        }
        self.history.insert(0, entry)
        if len(self.history) > 50:  # Лимит 50
            self.history = self.history[:50]
        self.save_history()
        self.update_history_table()

    def copy_password(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.password_var.get())
        messagebox.showinfo("Копировано", "Пароль скопирован в буфер обмена!")

    def update_history_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in self.history:
            self.tree.insert("", tk.END, values=(
            entry["date"], entry["password"][:30] + "..." if len(entry["password"]) > 30 else entry["password"],
            entry["length"]))

    def load_history(self):
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()