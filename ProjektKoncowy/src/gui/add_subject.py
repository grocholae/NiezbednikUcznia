import tkinter as tk
from tkinter import ttk, messagebox
from models.database import session, Subject
from tkinter.colorchooser import askcolor

class AddSubjectWindow:
    """
        Okno umożliwiające dodanie nowego przedmiotu.
        """

    def __init__(self, user):
        """
        :param user:
        """
        self.window = tk.Toplevel()
        self.window.title("Dodaj przedmiot")
        self.window.geometry("400x420")
        self.window.minsize(350, 350)
        self.window.configure(bg="#fff8f0")
        self.user = user

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TLabel", font=("Helvetica", 12), background="#fff8f0", foreground="#b3541e")
        style.configure("Custom.TButton", font=("Helvetica", 12), padding=6, background="#fff8f0", foreground="#b3541e")
        style.map("Custom.TButton", background=[("active", "#f0c8a6")], foreground=[("disabled", "#a0a0a0")])
        style.configure("Custom.TEntry", font=("Helvetica", 12), padding=5)

        # Konfiguracja grid dla głównego okna
        self.window.grid_rowconfigure(1, weight=1)   # lista i scrollbar rosną w pionie
        self.window.grid_columnconfigure(0, weight=1)  # cała szerokość rośnie

        # Tytuł
        title_lbl = tk.Label(self.window, text="Dodaj przedmiot", font=("Helvetica", 18, "bold"),
                             bg="#fff8f0", fg="#b3541e")
        title_lbl.grid(row=0, column=0, pady=(15, 10), sticky="n")

        # Lista przedmiotów ze scrollbarem
        list_frame = tk.Frame(self.window, bg="#fff8f0")
        list_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Grid konfiguracja dla list_frame — pozwala na rozciągnięcie listy i scrollbara
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.listbox = tk.Listbox(list_frame, height=10, yscrollcommand=scrollbar.set, width=50,
                                  font=("Helvetica", 11), bg="#fff8f0", fg="#b3541e",
                                  highlightthickness=0, relief="flat",
                                  selectbackground="#f0c8a6", selectforeground="#b3541e")
        self.listbox.grid(row=0, column=0, sticky="nsew")

        scrollbar.config(command=self.listbox.yview)

        # Formularz dodawania
        form_frame = tk.Frame(self.window, bg="#fff8f0")
        form_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        form_frame.grid_columnconfigure(1, weight=1)

        tk.Label(form_frame, text="Nazwa:", bg="#fff8f0", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(form_frame, width=40, style="Custom.TEntry")
        self.name_entry.grid(row=0, column=1, pady=5, sticky="ew")

        tk.Label(form_frame, text="Skrót:", bg="#fff8f0", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.nick_entry = ttk.Entry(form_frame, width=40, style="Custom.TEntry")
        self.nick_entry.grid(row=1, column=1, pady=5, sticky="ew")

        #kolor
        self.selected_color = "#FFFFFF"

        tk.Label(form_frame, text="Kolor:", bg="#fff8f0", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.color_display = tk.Label(form_frame, bg=self.selected_color, width=10, relief="sunken")
        self.color_display.grid(row=2, column=1, sticky="ew")

        self.color_button = ttk.Button(form_frame, text="Wybierz kolor", command=self.choose_color, style="Custom.TButton")
        self.color_button.grid(row=2, column=2, pady=5, ipadx=5,ipady=5, sticky="ew", padx=5)

        # Przycisk dodawania
        add_btn = ttk.Button(self.window, text="Dodaj", command=self.add_subject, style="Custom.TButton")
        add_btn.grid(row=3, column=0, pady=15, ipadx=10, ipady=5, sticky="ew", padx=20)

        self.refresh_subjects()

    def refresh_subjects(self):
        """
        Wyświetlanie bierzącej listy przedmiotów z bd.
        :return:
        """
        self.listbox.delete(0, tk.END)
        subjects = session.query(Subject).all()
        for subject in subjects:
            self.listbox.insert(tk.END, f"{subject.name} ({subject.nick})")

    def add_subject(self):
        """
        Dodawanie przedmiotu do bd.
        :return:
        """
        name = self.name_entry.get().strip()
        nick = self.nick_entry.get().strip()

        if not name or not nick:
            messagebox.showerror("Błąd", "Wypełnij oba pola.", parent=self.window)
            return

        existing = session.query(Subject).filter((Subject.name == name) | (Subject.nick == nick)).first()

        if existing:
            messagebox.showerror("Błąd", "Przedmiot o tej nazwie lub skrócie już istnieje.", parent=self.window)
            return

        new_subject = Subject(name=name, nick=nick,color=self.selected_color)
        session.add(new_subject)
        session.commit()
        self.name_entry.delete(0, tk.END)
        self.nick_entry.delete(0, tk.END)
        self.refresh_subjects()


    def choose_color(self):
        """
        Przypisanie koloru do przedmiotu - kwestia wizualna.
        :return:
        """
        color = askcolor(parent=self.window,title="Wybierz kolor przedmiotu", initialcolor=self.selected_color)
        if color[1]:  # jeśli użytkownik wybrał kolor, color[1] to HEX
            self.selected_color = color[1]
            self.color_display.config(bg=self.selected_color)