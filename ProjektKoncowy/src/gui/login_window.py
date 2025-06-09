import tkinter as tk
from tkinter import ttk,messagebox
from gui.register_window import RegisterWindow
from models.database import session, User
from utils.encryption import verify_password
from gui.dashboard import Dashboard

class LoginWindow:
    """
       Okno logowania użytkownika.
       Pozwala użytkownikowi wprowadzić nazwę użytkownika i hasło, a także umożliwia przejście do rejestracji nowego konta.
       """
    def __init__(self, master):
        """
        :param master:
        """
        self.master = master
        self.master.configure(bg="#fff8f0")
        self.master.minsize(350, 350)
        self.frame = tk.Frame(master, bg="#fff8f0")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TButton", font=("Helvetica", 12), padding=6, background="#fff8f0", foreground="#b3541e")
        style.map("Custom.TButton",
                  background=[("active", "#f0c8a6")],
                  foreground=[("disabled", "#a0a0a0")])
        style.configure("Custom.TLabel", font=("Helvetica", 14), background="#fff8f0", foreground="#b3541e")

        header = tk.Label(master, text="Niezbędnik Ucznia", font=("Helvetica", 24, "bold"), bg="#fff8f0", fg="#b3541e")
        header.place(relx=0.5, rely=0.3, anchor="center")

        #nazwa user
        username_lbl = ttk.Label(self.frame, text="Nazwa użytkownika", style="Custom.TLabel")
        username_lbl.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.username_entry = ttk.Entry(self.frame, width=40, font=("Helvetica", 14))
        self.username_entry.grid(row=1, column=0, pady=(0, 15))

        #haslo
        password_lbl = ttk.Label(self.frame, text="Hasło", style="Custom.TLabel")
        password_lbl.grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.password_entry = ttk.Entry(self.frame, show="*", width=40, font=("Helvetica", 14))
        self.password_entry.grid(row=3, column=0, pady=(0, 15))

        btn_frame = tk.Frame(self.frame, bg="#fff8f0")
        btn_frame.grid(row=4, column=0, pady=(10, 0))

        self.login_btn = ttk.Button(btn_frame, text="Zaloguj", command=self.login, style="Custom.TButton")
        self.login_btn.pack(side="left", padx=10, ipadx=10, ipady=5)

        self.register_btn = ttk.Button(btn_frame, text="Zarejestruj", command=self.register, style="Custom.TButton")
        self.register_btn.pack(side="left", padx=10, ipadx=10, ipady=5)

        # podpisały się
        creators_lbl = tk.Label(master, text="Twórcy: Ewa Grochola, Ula Kępka", font=("Helvetica", 8),
                                bg="#fff8f0", fg="#888")
        creators_lbl.place(relx=0.98, rely=0.98, anchor="se")

    def login(self):
        """
        Logowanie ze sprawdzeniem zahashowanego hasła. Sprawdzenie z bd, czy istnieje taki user.
        :return:
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = session.query(User).filter_by(username=username).first()
        if user and verify_password(password, user.password_hash):
            messagebox.showinfo("Sukces", "Zalogowano pomyślnie!")
            self.frame.destroy()
            Dashboard(self.master, user)
        else:
            messagebox.showerror("Błąd", "Niepoprawne dane logowania.")

    def register(self):
        """
        Dodanie opcji rejestracji nowego użytkownika. Metoda wywołuje osobą klasę.
        :return:
        """
        RegisterWindow(self.master, self)