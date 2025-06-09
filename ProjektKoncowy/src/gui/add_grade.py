import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from models.database import Student, Grade, Subject, Schedule, session

class AddGradeWindow:
    """
       Okno umożliwiające nauczycielowi wystawienie oceny studentowi.
       """

    def __init__(self, user):
        """
        :param user:
        """
        self.window = tk.Toplevel()
        self.window.title("Wystaw ocenę")
        self.window.geometry("350x400")
        self.window.minsize(320, 380)
        self.window.configure(bg="#fff8f0")
        self.user = user

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TLabel", font=("Helvetica", 12), background="#fff8f0", foreground="#b3541e")
        style.configure("Title.TLabel", font=("Helvetica", 18, "bold"), background="#fff8f0", foreground="#b3541e")
        style.configure("Custom.TMenubutton", font=("Helvetica", 12), background="#fff8f0", foreground="#b3541e", padding=6)
        style.configure("Custom.TButton", font=("Helvetica", 12), padding=6, background="#fff8f0", foreground="#b3541e")
        style.map("Custom.TButton", background=[("active", "#f0c8a6")], foreground=[("disabled", "#a0a0a0")])

        # Tytuł okna
        title_lbl = ttk.Label(self.window, text="Wystaw ocenę", style="Title.TLabel")
        title_lbl.pack(pady=(15, 10))

        # Pobranie studentów przypisanych do nauczyciela
        self.students = (
            session.query(Student)
            .join(Schedule)
            .filter(Schedule.teacher_id == self.user.id)
            .distinct()
            .all()
        )

        self.student_var = tk.StringVar()
        student_names = [f"{s.first_name} {s.last_name}" for s in self.students]
        ttk.Label(self.window, text="Wybierz studenta:", style="Custom.TLabel").pack(anchor="w", padx=20)

        self.student_menu = ttk.OptionMenu(self.window, self.student_var, student_names[0] if student_names else "", *student_names,
                                           command=self.update_subjects)
        self.student_menu.config(style="Custom.TMenubutton")
        self.student_menu.pack(fill="x", padx=20, pady=5)

        # Przedmioty
        self.subject_var = tk.StringVar()
        ttk.Label(self.window, text="Wybierz przedmiot:", style="Custom.TLabel").pack(anchor="w", padx=20)

        self.subject_menu = ttk.OptionMenu(self.window, self.subject_var, "")
        self.subject_menu.config(style="Custom.TMenubutton")
        self.subject_menu.pack(fill="x", padx=20, pady=5)

        # Ocena
        ttk.Label(self.window, text="Ocena:", style="Custom.TLabel").pack(anchor="w", padx=20)
        self.grade_var = tk.StringVar()
        grade_choices = ["2.0", "3.0", "3.5", "4.0", "4.5", "5.0"]
        grade_menu = ttk.OptionMenu(self.window, self.grade_var, grade_choices[0], *grade_choices)
        grade_menu.config(style="Custom.TMenubutton")
        grade_menu.pack(fill="x", padx=20, pady=5)

        # Data oceny
        ttk.Label(self.window, text="Data:", style="Custom.TLabel").pack(anchor="w", padx=20)
        self.date_entry = ttk.Entry(self.window)
        self.date_entry.insert(0, date.today().isoformat())
        self.date_entry.pack(fill="x", padx=20, pady=5)

        # Przycisk zapisu oceny
        add_btn = ttk.Button(self.window, text="Dodaj ocenę", command=self.save_grade, style="Custom.TButton")
        add_btn.pack(pady=20, ipadx=10, ipady=5)

        if self.students:
            self.student_var.set(student_names[0])
            self.update_subjects(student_names[0])
        else:
            messagebox.showinfo("Brak danych", "Brak studentów przypisanych do Twoich grup.")

    def update_subjects(self, selected_student_name):
        """
        Aktualizuje listę przedmiotów dostępnych dla wybranego studenta.
        """
        selected_student = next((s for s in self.students if f"{s.first_name} {s.last_name}" == selected_student_name),
                                None)
        if not selected_student:
            return

        # Pobranie przedmiotów prowadzonych przez nauczyciela dla tego studenta
        subject_ids = (
            session.query(Schedule.subject_id)
            .filter(Schedule.teacher_id == self.user.id, Schedule.student_id == selected_student.id)
            .distinct()
            .all()
        )
        subject_ids = [sid[0] for sid in subject_ids]
        subjects = session.query(Subject).filter(Subject.id.in_(subject_ids)).all()

        self.subjects = subjects
        subject_names = [s.name for s in subjects]

        menu = self.subject_menu['menu']
        menu.delete(0, 'end')
        for name in subject_names:
            menu.add_command(label=name, command=tk._setit(self.subject_var, name))

        if subject_names:
            self.subject_var.set(subject_names[0])
        else:
            self.subject_var.set("")

    def save_grade(self):
        """
        Zapisuje wystawioną ocenę do bazy danych po weryfikacji danych formularza.
        """
        student_name = self.student_var.get()
        subject_name = self.subject_var.get()
        grade_value = self.grade_var.get()
        grade_date = self.date_entry.get()

        student = next((s for s in self.students if f"{s.first_name} {s.last_name}" == student_name), None)
        subject = next((s for s in self.subjects if s.name == subject_name), None)

        if not all([student, subject, grade_value]):
            messagebox.showerror("Błąd", "Uzupełnij wszystkie dane.")
            return

        try:
            parsed_date = date.fromisoformat(grade_date)
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowy format daty (RRRR-MM-DD).")
            return

        new_grade = Grade(
            grade=float(grade_value),
            date=parsed_date,
            student=student,
            teacher=self.user,
            subject=subject
        )
        session.add(new_grade)
        session.commit()
        messagebox.showinfo("Sukces", f"Ocenę {grade_value} dodano dla {student.first_name} {student.last_name}.")
        self.window.destroy()