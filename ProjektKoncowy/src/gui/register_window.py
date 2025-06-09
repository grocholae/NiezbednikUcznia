import tkinter as tk
from tkinter import messagebox,ttk
from models.database import session, User, Student, Teacher
from utils.encryption import hash_password

class RegisterWindow:
    """
        Okno rejestracji nowego użytkownika. Pozwala na wprowadzenie danych użytkownika..
        """

    def __init__(self, master, login_window):
        """
        :param master:
        :param login_window:
        """
        self.login_window = login_window
        self.top = tk.Toplevel(master)
        self.top.title("Rejestracja")
        self.top.configure(bg="#fff8f0")
        self.top.minsize(400, 350)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TButton",font=("Helvetica", 12), padding=6,background="#fff8f0",foreground="#b3541e")
        style.map("Custom.TButton", background=[("active", "#f0c8a6")],foreground=[("disabled", "#a0a0a0")])
        style.configure("Custom.TLabel",font=("Helvetica", 14), background="#fff8f0",foreground="#b3541e")
        style.configure("Custom.TMenubutton", font=("Helvetica", 12),background="#fff8f0",foreground="#b3541e",relief="flat", padding=5)
        style.map("Custom.TMenubutton", background=[("active", "#f0c8a6")],foreground=[("disabled", "#a0a0a0")])

        frame = tk.Frame(self.top, bg="#fff8f0")
        frame.pack(padx=20, pady=20)

        # Nazwa użytkownika
        username_lbl = ttk.Label(frame, text="Nazwa użytkownika", style="Custom.TLabel")
        username_lbl.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=(0, 10))

        # Hasło
        password_lbl = ttk.Label(frame, text="Hasło", style="Custom.TLabel")
        password_lbl.grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.password_entry = ttk.Entry(frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, pady=(0, 10))

        # Imię
        first_name_lbl = ttk.Label(frame, text="Imię", style="Custom.TLabel")
        first_name_lbl.grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.first_name_entry = ttk.Entry(frame, width=30)
        self.first_name_entry.grid(row=2, column=1, pady=(0, 10))

        # Nazwisko
        last_name_lbl = ttk.Label(frame, text="Nazwisko", style="Custom.TLabel")
        last_name_lbl.grid(row=3, column=0, sticky="w", pady=(0, 5))
        self.last_name_entry = ttk.Entry(frame, width=30)
        self.last_name_entry.grid(row=3, column=1, pady=(0, 10))

        # Rola
        role_lbl = ttk.Label(frame, text="Rola", style="Custom.TLabel")
        role_lbl.grid(row=4, column=0, sticky="w", pady=(0, 5))
        self.role_var = tk.StringVar()
        self.role_var.set("student")

        role_menu = ttk.OptionMenu(frame, self.role_var, "student", "student", "teacher")
        role_menu.config(style="Custom.TMenubutton")
        role_menu.grid(row=4, column=1, pady=(0, 10), sticky="ew")

        register_btn = ttk.Button(frame, text="Zarejestruj", command=self.register_user, style="Custom.TButton")
        register_btn.grid(row=5, column=0, columnspan=2, pady=15, sticky="ew")

    def register_user(self):
        """
        Dodanie użytkownika do bd.
        :return:
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        role = self.role_var.get()

        if not all([username, password, first_name, last_name]):
            messagebox.showerror("Błąd", "Wszystkie pola są wymagane.", parent=self.top)
            return

        if session.query(User).filter_by(username=username).first():
            messagebox.showerror("Błąd", "Użytkownik już istnieje.", parent=self.top)
            return

        hashed = hash_password(password)

        if role == "student":
            user = Student(username=username, password_hash=hashed, first_name=first_name, last_name=last_name,
                           role=role)
        else:
            user = Teacher(username=username, password_hash=hashed, first_name=first_name, last_name=last_name,
                           role=role)

        session.add(user)
        session.commit()
        messagebox.showinfo("Sukces", f"Użytkownik {role} zarejestrowany.", parent=self.top)
        self.login_window.username_entry.delete(0, tk.END)
        self.login_window.password_entry.delete(0, tk.END)
        self.top.destroy()