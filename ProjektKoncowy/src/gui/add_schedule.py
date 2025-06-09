import tkinter as tk
from tkinter import ttk
from models.database import session, Group, Subject, Time
from models.database import Schedule

class AddScheduleWindow:
    """
        Okno dodawania zajęć do planu użytkownika.
        """

    def __init__(self, user):
        """
        :param user:
        """
        self.window = tk.Toplevel()
        self.window.title("Dodaj zajęcia")
        self.window.geometry("360x450")
        self.window.minsize(340, 420)
        self.window.configure(bg="#fff8f0")
        self.user = user

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TLabel", font=("Helvetica", 12),background="#fff8f0",foreground="#b3541e")
        style.configure("Custom.TButton", font=("Helvetica", 12), padding=6, background="#fff8f0", foreground="#b3541e")
        style.map("Custom.TButton", background=[("active", "#f0c8a6")], foreground=[("disabled", "#a0a0a0")])
        style.configure("Custom.TMenubutton",font=("Helvetica", 12), background="#fff8f0", foreground="#b3541e", relief="flat", padding=5)
        style.map("Custom.TMenubutton", background=[("active", "#f0c8a6")],foreground=[("disabled", "#a0a0a0")])

        # Tytuł
        title_lbl = tk.Label(self.window, text="Dodaj zajęcia", font=("Helvetica", 18, "bold"),bg="#fff8f0", fg="#b3541e")
        title_lbl.pack(pady=(15, 15))

        # Dzień tygodnia
        self.day_var = tk.StringVar()
        days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
        ttk.Label(self.window, text="Dzień tygodnia:", style="Custom.TLabel").pack(anchor="w", padx=20)
        day_menu = ttk.OptionMenu(self.window, self.day_var, days[0], *days)
        day_menu.config(style="Custom.TMenubutton")
        day_menu.pack(fill="x", padx=20, pady=5)

        # Przedmiot
        ttk.Label(self.window, text="Przedmiot:", style="Custom.TLabel").pack(anchor="w", padx=20)
        self.subjects = session.query(Subject).all()
        self.subject_var = tk.StringVar()
        subject_names = [s.name for s in self.subjects]
        subject_menu = ttk.OptionMenu(self.window, self.subject_var, subject_names[0], *subject_names, command=self.update_teachers)
        subject_menu.config(style="Custom.TMenubutton")
        subject_menu.pack(fill="x", padx=20, pady=5)

        # Grupa
        ttk.Label(self.window, text="Grupa:", style="Custom.TLabel").pack(anchor="w", padx=20)
        self.groups = session.query(Group).all()
        self.group_var = tk.StringVar()
        group_names = [g.name for g in self.groups]
        group_menu = ttk.OptionMenu(self.window, self.group_var, group_names[0], *group_names)
        group_menu.config(style="Custom.TMenubutton")
        group_menu.pack(fill="x", padx=20, pady=5)

        # Nauczyciel
        ttk.Label(self.window, text="Nauczyciel:", style="Custom.TLabel").pack(anchor="w", padx=20)
        self.teacher_var = tk.StringVar()
        self.teacher_menu = ttk.OptionMenu(self.window, self.teacher_var, "")
        self.teacher_menu.config(style="Custom.TMenubutton")
        self.teacher_menu.pack(fill="x", padx=20, pady=5)

        # Godzina
        ttk.Label(self.window, text="Godzina:", style="Custom.TLabel").pack(anchor="w", padx=20)
        self.times = session.query(Time).all()
        self.time_var = tk.StringVar()
        self.time_menu = ttk.OptionMenu(self.window, self.time_var, "")
        self.time_menu.config(style="Custom.TMenubutton")
        self.time_menu.pack(fill="x", padx=20, pady=5)

        # Przycisk dodawania
        add_btn = ttk.Button(self.window, text="Dodaj", command=self.add_schedule, style="Custom.TButton")
        add_btn.pack(pady=20, ipadx=10, ipady=5)

        # menu
        self.teachers = []
        self.update_teachers(self.subject_var.get())
        self.day_var.trace_add("write", lambda *_: self.update_times())
        self.group_var.trace_add("write", lambda *_: self.update_times())
        self.teacher_var.trace_add("write", lambda *_: self.update_times())
        self.update_times()

    def add_schedule(self):
        """
        Dodanie do bd nowych zajęć.
        :return:
        """
        day = self.day_var.get()
        subject = next((s for s in self.subjects if s.name == self.subject_var.get()), None)
        teacher = next((t for t in self.teachers if f"{t.first_name} {t.last_name}" == self.teacher_var.get()), None)
        time = next((t for t in self.times if t.time == self.time_var.get()), None)
        group = next((g for g in self.groups if g.name == self.group_var.get()), None)

        if not all([subject, teacher, time, group]):
            print("Błąd: brak danych")
            return

        for student in group.students:
            new_schedule = Schedule(
                day=day,
                subject=subject,
                student=student,
                teacher=teacher,
                time=time
            )
            session.add(new_schedule)

        session.commit()
        self.window.destroy()

    def update_teachers(self, selected_subject_name):
        """
        Wyświetlanie nauczycieli uczących wybrany przedmiot.
        :param selected_subject_name:
        :return:
        """
        selected_subject = next((s for s in self.subjects if s.name == selected_subject_name), None)
        if not selected_subject:
            return

        teachers = selected_subject.teachers
        teacher_names = [f"{t.first_name} {t.last_name}" for t in teachers]

        self.teacher_menu['menu'].delete(0, 'end')
        for name in teacher_names:
            self.teacher_menu['menu'].add_command(label=name, command=tk._setit(self.teacher_var, name))

        if teacher_names:
            self.teacher_var.set(teacher_names[0])
        else:
            self.teacher_var.set("")

        self.teachers = teachers

    def update_times(self, *_):
        """
        Wyświetlanie czasu dostępności dla grupy, dnia tygodnia oraz nauczyciela łącznie.
        :param _:
        :return:
        """
        selected_day = self.day_var.get()
        selected_teacher = next((t for t in self.teachers if f"{t.first_name} {t.last_name}" == self.teacher_var.get()),None)
        selected_group = next((g for g in self.groups if g.name == self.group_var.get()), None)

        if not (selected_day and selected_teacher and selected_group):
            return

        group_students_ids = [s.id for s in selected_group.students]
        occupied_times = set()
        teacher_schedules = session.query(Schedule).filter_by(day=selected_day, teacher=selected_teacher).all()
        occupied_times.update([s.time_id for s in teacher_schedules])

        group_schedules = (session.query(Schedule)
                           .filter(Schedule.day == selected_day, Schedule.student_id.in_(group_students_ids)).all())
        occupied_times.update([s.time_id for s in group_schedules])

        available_times = [t for t in self.times if t.id not in occupied_times]
        self.time_menu['menu'].delete(0, 'end')
        for t in available_times:
            self.time_menu['menu'].add_command(label=t.time, command=tk._setit(self.time_var, t.time))

        if available_times:
            self.time_var.set(available_times[0].time)
        else:
            self.time_var.set("Brak dostępnych godzin")

