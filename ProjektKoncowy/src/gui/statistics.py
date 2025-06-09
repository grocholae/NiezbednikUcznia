import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from models.database import session, Grade
from collections import defaultdict

class StatisticsWindow:
    """
    Okno statystyk ocen dla studenta.

    Ta klasa tworzy okno w tkinter, które wyświetla średnią ocen oraz wykres słupkowy
    z ocenami pogrupowanymi według przedmiotów. Dodatkowo umożliwia eksport wykresu do pliku PDF.

    :param user: Obiekt reprezentujący użytkownika (studenta), dla którego wyświetlane są statystyki.
    :type user: User

    Atrybuty:
        user (User): Obiekt użytkownika.
        window (tk.Toplevel): Główne okno statystyk.
        grades (list of Grade): Lista ocen studenta pobrana z bazy danych.
    """

    def __init__(self, user):
        """
        Inicjalizuje okno statystyk dla podanego użytkownika.

        :param user: Obiekt użytkownika (studenta).
        :type user: User
        """
        self.user = user
        self.window = tk.Toplevel()
        self.window.title("Statystyki ucznia")
        self.window.geometry("700x500")
        self.window.minsize(600, 400)
        self.window.configure(bg="#fff8f0")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)  # wykres rozciąga się

        self.grades = session.query(Grade).filter_by(student_id=self.user.id).all()

        # Tytuł
        title_lbl = tk.Label(self.window, text="Statystyki ucznia", font=("Helvetica", 18, "bold"),
                             bg="#fff8f0", fg="#b3541e")
        title_lbl.grid(row=0, column=0, pady=(15, 5), sticky="n")

        # Średnia ocen
        avg_frame = tk.Frame(self.window, pady=10, bg="#fff8f0")
        avg_frame.grid(row=2, column=0, sticky="n", padx=20)
        avg = self.calculate_average()
        tk.Label(avg_frame, text="Średnia ocen:", font=("Helvetica", 14), bg="#fff8f0").pack()
        tk.Label(avg_frame, text=f"{avg:.2f}", font=("Helvetica", 36, "bold"), fg="#2c3e50", bg="#fff8f0").pack()

        # Wykres
        chart_frame = tk.LabelFrame(self.window, text="Oceny wg przedmiotów", padx=10,
                                    pady=10, bg="#fff8f0", fg="#b3541e", font=("Helvetica", 12, "bold"))
        chart_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.show_chart(chart_frame)

        # Sekcja: Przycisk eksportu
        btn_frame = tk.Frame(self.window, bg="#fff8f0")
        btn_frame.grid(row=3, column=0, pady=15)
        export_btn = tk.Button(btn_frame, text="Eksportuj do PDF", command=self.export,
                               bg="#d0a96f", fg="white", font=("Helvetica", 12, "bold"), relief="raised", padx=10, pady=5)
        export_btn.pack(pady=(10, 0))

    def show_chart(self, parent):
        """
        Wyświetla wykres słupkowy średnich ocen według przedmiotów w podanym kontenerze.

        Jeśli brak ocen, wyświetla stosowny komunikat.

        :param parent: Kontener tkinter, w którym zostanie osadzony wykres.
        :type parent: tk.Widget
        """
        if not self.grades:
            tk.Label(parent, text="Brak ocen do wyświetlenia.", font=("Helvetica", 12), fg="gray", bg="#fff8f0").pack()
            return

        subjects, averages = average_grades_by_subject(self.grades)

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(subjects, averages, color="#3498db")
        ax.set_ylim(1, 6)
        ax.set_title("Wykres ocen wg przedmiotów", fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def calculate_average(self):
        """
        Oblicza średnią ocen studenta.

        :return: Średnia ocen lub 0.0 jeśli brak ocen.
        :rtype: float
        """
        if not self.grades:
            return 0.0
        return sum(g.grade for g in self.grades) / len(self.grades)

    def export(self):
        """
        Eksportuje wykres ocen do pliku PDF.

        Plik zapisywany jest w katalogu `raporty/` z nazwą zawierającą ID i imię oraz nazwisko użytkownika.
        Jeśli brak ocen, wyświetla komunikat informujący o braku danych do eksportu.
        """
        if not self.grades:
            messagebox.showinfo("Eksport", "Brak ocen do wyeksportowania.")
            return

        subjects, averages = average_grades_by_subject(self.grades)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(subjects, averages, color="#3498db")
        ax.set_ylim(1, 6)
        ax.set_title(f"Wykres ocen dla {self.user.first_name} {self.user.last_name}", fontsize=16)

        filename = f"wykres_statystyk_{self.user.id}_{sanitize_filename_component(self.user.first_name)}_{sanitize_filename_component(self.user.last_name)}.pdf"
        if not os.path.exists("raporty"):
            os.makedirs("raporty")
        filepath = os.path.join("raporty", filename)
        fig.savefig(filepath, bbox_inches="tight")
        plt.close(fig)

        messagebox.showinfo("Eksport", f"Statystyki zapisano do pliku:\n{filename}")


def sanitize_filename_component(s):
    """
    Zamienia niedozwolone znaki w nazwie pliku na bezpieczne.

    Aktualnie zastępuje spacje i znaki '/' podkreśleniami.

    :param s: Ciąg znaków do sanitizacji.
    :type s: str
    :return: Sanitizowany ciąg znaków.
    :rtype: str
    """
    return str(s).replace(" ", "_").replace("/", "_")


def average_grades_by_subject(grades):
    """
    Oblicza średnie oceny dla każdego przedmiotu.

    :param grades: Lista obiektów oceny.
    :type grades: list of Grade
    :return: Krotka dwóch list: (lista nazw przedmiotów, lista średnich ocen).
    :rtype: tuple[list[str], list[float]]
    """
    subject_grades = defaultdict(list)
    for g in grades:
        subject_grades[g.subject.nick].append(g.grade)
    subjects = []
    averages = []
    for subject, grades_list in subject_grades.items():
        subjects.append(subject)
        averages.append(sum(grades_list) / len(grades_list))
    return subjects, averages