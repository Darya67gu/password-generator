import random
import string
import tkinter as tk
from tkinter import ttk, messagebox

# ==================== ФУНКЦИИ ГЕНЕРАЦИИ ====================

def generate_single_password(length, use_lower, use_upper, use_digits, use_symbols):
    """Генерация одного пароля по заданным параметрам"""
    chars = ""
    
    if use_lower:
        chars += string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
    
    # Если ничего не выбрано, используем хотя бы строчные буквы
    if not chars:
        chars = string.ascii_lowercase
    
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def generate_passwords(count, length, use_lower, use_upper, use_digits, use_symbols):
    """Генерация списка паролей"""
    passwords = []
    for _ in range(count):
        passwords.append(generate_single_password(length, use_lower, use_upper, use_digits, use_symbols))
    return passwords

# ==================== ГРАФИЧЕСКОЕ ПРИЛОЖЕНИЕ ====================

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор пароля")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)
        
        self.current_passwords = []
        self.build_ui()
        self.generate()
    
    def build_ui(self):
        # Заголовок
        title = tk.Label(self.root, text="Генератор пароля", 
                        font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333333")
        title.pack(pady=15)
        
        # Подзаголовок
        subtitle = tk.Label(self.root, 
            text="Сгенерируйте список надежных паролей, ключей и промокодов\nна основе алгоритма случайных чисел по вашим параметрам",
            font=("Arial", 9), bg="#f0f0f0", fg="#666666", justify="center")
        subtitle.pack(pady=5)
        
        # Рамка с настройками
        settings_frame = tk.LabelFrame(self.root, text="Параметры генерации", 
                                       font=("Arial", 10, "bold"),
                                       bg="#f0f0f0", fg="#333333", padx=15, pady=10)
        settings_frame.pack(pady=10, padx=20, fill="x")
        
        # Длина пароля
        length_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        length_frame.pack(fill="x", pady=5)
        
        tk.Label(length_frame, text="Длина пароля:", font=("Arial", 10),
                bg="#f0f0f0", fg="#333333", width=15, anchor="w").pack(side="left")
        
        self.length_var = tk.IntVar(value=10)
        self.length_spin = tk.Spinbox(length_frame, from_=6, to=32, width=8,
                                      textvariable=self.length_var, font=("Arial", 10))
        self.length_spin.pack(side="left", padx=5)
        
        tk.Label(length_frame, text="Количество паролей:", font=("Arial", 10),
                bg="#f0f0f0", fg="#333333", width=15, anchor="w").pack(side="left", padx=(20,0))
        
        self.count_var = tk.IntVar(value=5)
        self.count_spin = tk.Spinbox(length_frame, from_=1, to=50, width=8,
                                     textvariable=self.count_var, font=("Arial", 10))
        self.count_spin.pack(side="left", padx=5)
        
        # Строчные буквы
        lower_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        lower_frame.pack(fill="x", pady=5)
        
        tk.Label(lower_frame, text="Строчные буквы:", font=("Arial", 10),
                bg="#f0f0f0", fg="#333333", width=15, anchor="w").pack(side="left")
        
        self.use_lower = tk.BooleanVar(value=True)
        tk.Radiobutton(lower_frame, text="Да", variable=self.use_lower, value=True,
                      bg="#f0f0f0", font=("Arial", 9)).pack(side="left", padx=5)
        tk.Radiobutton(lower_frame, text="Нет", variable=self.use_lower, value=False,
                      bg="#f0f0f0", font=("Arial", 9)).pack(side="left", padx=5)
        
        # Заглавные буквы
        upper_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        upper_frame.pack(fill="x", pady=5)
        
        tk.Label(upper_frame, text="Заглавные буквы:", font=("Arial", 10),
                bg="#f0f0f0", fg="#333333", width=15, anchor="w").pack(side="left")
        
        self.use_upper = tk.BooleanVar(value=True)
        tk.Radiobutton(upper_frame, text="Да", variable=self.use_upper, value=True,
                      bg="#f0f0f0", font=("Arial", 9)).pack(side="left", padx=5)
        tk.Radiobutton(upper_frame, text="Нет", variable=self.use_upper, value=False,
                      bg="#f0f0f0", font=("Arial", 9)).pack(side="left", padx=5)
        
        # Цифры
        digits_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        digits_frame.pack(fill="x", pady=5)
        
        tk.Label(digits_frame, text="Цифры:", font=("Arial", 10),
                bg="#f0f0f0", fg="#333333", width=15, anchor="w").pack(side="left")
        
        self.use_digits = tk.BooleanVar(value=True)
        tk.Radiobutton(digits_frame, text="Да", variable=self.use_digits, value=True,
                      bg="#f0f0f0", font=("Arial", 9)).pack(side="left", padx=5)
        tk.Radiobutton(digits_frame, text="Нет", variable=self.use_digits, value=False,
                      bg="#f0f0f0", font=("Arial", 9)).pack(side="left", padx=5)
        
        # Знаки (спецсимволы)
        symbols_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        symbols_frame.pack(fill="x", pady=5)
        
        tk.Label(symbols_frame, text="Знаки:", font=("Arial", 10),
                bg="#f0f0f0", fg="#333333", width=15, anchor="w").pack(side="left")
        
        self.use_symbols = tk.BooleanVar(value=False)
        tk.Radiobutton(symbols_frame, text="Да", variable=self.use_symbols, value=True,
                      bg="#f0f0f0", font=("Arial", 9)).pack(side="left", padx=5)
        tk.Radiobutton(symbols_frame, text="Нет", variable=self.use_symbols, value=False,
                      bg="#f0f0f0", font=("Arial", 9)).pack(side="left", padx=5)
        
        # Кнопки
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=15)
        
        btn_generate = tk.Button(btn_frame, text="Сгенерировать", 
                                command=self.generate,
                                bg="#4a90e2", fg="white", font=("Arial", 11, "bold"),
                                width=15, height=1, relief="flat")
        btn_generate.pack(side="left", padx=10)
        
        btn_refresh = tk.Button(btn_frame, text="Обновить", 
                               command=self.refresh,
                               bg="#6c757d", fg="white", font=("Arial", 11, "bold"),
                               width=15, height=1, relief="flat")
        btn_refresh.pack(side="left", padx=10)
        
        # Рамка для результатов
        result_frame = tk.LabelFrame(self.root, text="Сгенерированные пароли", 
                                     font=("Arial", 10, "bold"),
                                     bg="#f0f0f0", fg="#333333", padx=10, pady=10)
        result_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Фрейм для текстового поля
        text_frame = tk.Frame(result_frame, bg="#f0f0f0")
        text_frame.pack(fill="both", expand=True)
        
        # Текстовое поле для вывода паролей (редактируемое, чтобы можно было выделять)
        self.result_text = tk.Text(text_frame, height=12, width=60,
                                   font=("Arial", 11), bg="white", fg="#333333",
                                   wrap="word", relief="sunken", bd=1,
                                   selectbackground="#4a90e2")  # Синее выделение
        self.result_text.pack(side="left", fill="both", expand=True)
        
        # Скроллбар
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.result_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # Контекстное меню для копирования
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Копировать", command=self.copy_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Выделить всё", command=self.select_all)
        
        # Привязываем события
        self.result_text.bind("<Button-3>", self.show_context_menu)  # ПКМ
        self.result_text.bind("<Control-c>", self.copy_selected)     # Ctrl+C
        self.result_text.bind("<Control-a>", self.select_all)        # Ctrl+A
        
        # Информационная подсказка
        hint_frame = tk.Frame(result_frame, bg="#f0f0f0")
        hint_frame.pack(fill="x", pady=(5,0))
        
        hint_label = tk.Label(hint_frame, text="💡 Как скопировать пароль: выделите мышкой нужный пароль → Ctrl+C или ПКМ → Копировать", 
                             font=("Arial", 8), bg="#f0f0f0", fg="#888888")
        hint_label.pack()
        
        # Статус
        self.status_label = tk.Label(self.root, text="Готов к генерации", 
                                     font=("Arial", 8), bg="#f0f0f0", fg="#888888")
        self.status_label.pack(pady=5)
    
    def copy_selected(self, event=None):
        """Копировать выделенный текст в буфер обмена"""
        try:
            # Пытаемся получить выделенный текст
            selected_text = self.result_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            
            if selected_text:
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
                self.root.update()
                
                # Показываем временное сообщение
                self.status_label.config(text=f"✓ Скопировано: {selected_text[:30]}{'...' if len(selected_text) > 30 else ''}", fg="#28a745")
                self.root.after(2000, lambda: self.status_label.config(text="Готов к генерации", fg="#888888"))
            else:
                self.status_label.config(text="❌ Сначала выделите нужный пароль мышкой", fg="#dc3545")
                self.root.after(2000, lambda: self.status_label.config(text="Готов к генерации", fg="#888888"))
        except tk.TclError:
            # Ничего не выделено
            self.status_label.config(text="❌ Сначала выделите нужный пароль мышкой", fg="#dc3545")
            self.root.after(2000, lambda: self.status_label.config(text="Готов к генерации", fg="#888888"))
    
    def select_all(self, event=None):
        """Выделить весь текст"""
        self.result_text.tag_add(tk.SEL, "1.0", tk.END)
        self.result_text.mark_set(tk.INSERT, "1.0")
        self.result_text.see(tk.INSERT)
        return "break"  # Предотвращаем стандартное поведение
    
    def show_context_menu(self, event):
        """Показать контекстное меню при ПКМ"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def generate(self):
        """Генерация паролей"""
        length = self.length_var.get()
        count = self.count_var.get()
        use_lower = self.use_lower.get()
        use_upper = self.use_upper.get()
        use_digits = self.use_digits.get()
        use_symbols = self.use_symbols.get()
        
        # Проверка: хотя бы один тип символов должен быть выбран
        if not (use_lower or use_upper or use_digits or use_symbols):
            messagebox.showwarning("Предупреждение", "Выберите хотя бы один тип символов!")
            return
        
        # Генерация
        self.current_passwords = generate_passwords(count, length, use_lower, use_upper, use_digits, use_symbols)
        
        # Отображение
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        
        for i, pwd in enumerate(self.current_passwords, 1):
            self.result_text.insert(tk.END, f"{i}. {pwd}\n")
        
        self.result_text.config(state="normal")  # Оставляем редактируемым для копирования
        self.status_label.config(text=f"Сгенерировано {count} паролей длиной {length} символов", fg="#888888")
    
    def refresh(self):
        """Обновить (перегенерировать те же параметры)"""
        self.generate()

# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()