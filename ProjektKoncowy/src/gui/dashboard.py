import tkinter as tk
from tkinter import ttk
from gui.add_grade import AddGradeWindow
from gui.add_schedule import AddScheduleWindow
from gui.add_subject import AddSubjectWindow
from gui.assign_student_group import AssignStudentWindow
from gui.assign_teacher_subject import AssignTeacherWindow
from gui.schedule import ScheduleWindow
from gui.grades import GradesWindow
from gui.schedule_teacher import TeacherScheduleWindow
from gui.statistics import StatisticsWindow


class Dashboard:
    """
       Klasa reprezentująca główne okno pulpitu użytkownika po zalogowaniu.

       Zależnie od roli użytkownika (student, nauczyciel, admin), wyświetla odpowiednie przyciski
       do nawigacji po funkcjach systemu. Zawiera również przycisk „Wyloguj”, który pozwala wrócić
       do ekranu logowania.

       """

    def __init__(self, master, user):
        """
        :param master:
        :param user:
        """
        self.user = user
        self.master = master
        self.schedule_window = None
        self.grades_window = None
        self.statistics_window = None
        self.add_schedule_window = None
        self.assign_student_window = None
        self.add_subject_window = None
        self.assign_teacher_window = None
        self.add_grades_window = None
        self.master.minsize(350, 350)
        self.master.configure(bg="#fff8f0")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TButton", font=("Helvetica", 12), padding=6, background="#fff8f0")
        style.map("Custom.TButton",
                  background=[("active", "#f0e0d6")],
                  foreground=[("disabled", "#a0a0a0")])
        style.configure("Custom.TLabel", font=("Helvetica", 14), background="#fff8f0")

        self.frame = tk.Frame(master, bg="#fff8f0")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        greeting = ttk.Label(self.frame, text=f"Witaj, {user.username}!", style="Custom.TLabel", anchor="center")
        greeting.pack(pady=(0, 20), fill="x")

        button_kwargs = {
            "style": "Custom.TButton",
            "width": 30
        }

        def add_button(text, command):
            """
            Opcja dodania dla odpowiedniej roli użytkownika danych funkcji.
            :param text:
            :param command:
            :return:
            """
            btn = ttk.Button(self.frame, text=text, command=command, **button_kwargs)
            btn.pack(pady=5, fill="x")

        # STUDENT
        if user.role == 'student':
            add_button("Plan lekcji", self.open_schedule)
            add_button("Dziennik ocen", self.open_grades)
            add_button("Statystyki", self.open_statistics)

        # ADMIN
        if user.role == 'admin':
            add_button("Dodaj studenta do grupy", self.open_assign_student)
            add_button("Dodaj plan zajęć", self.open_add_schedule)
            add_button("Dodaj przedmiot", self.open_add_subject)
            add_button("Dodaj nauczyciela do przedmiotu", self.open_assign_teacher)

        # TEACHER
        if user.role == 'teacher':
            add_button("Dodaj ocenę studentowi", self.open_add_grade)
            add_button("Plan zajęć", self.open_schedule_teacher)

        logout_btn = ttk.Button(master, text="Wyloguj", command=self.logout, style="Custom.TButton")
        logout_btn.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

    def logout(self):
        """Wylogowuje użytkownika: niszczy ramkę dashboardu i odtwarza LoginWindow.
        :return:
        """
        self.frame.destroy()
        for widget in self.master.place_slaves():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Wyloguj":
                widget.destroy()
        from gui.login_window import LoginWindow  #bo nie można było  globalnych ref dla obu
        LoginWindow(self.master)

    # STUDENT
    def open_schedule(self):
        """Otwiera okno z planem lekcji (dla studentów).
        :return: """
        if self.schedule_window is None or not self.schedule_window.window.winfo_exists():
            self.schedule_window = ScheduleWindow(self.user)
        else:
            self.schedule_window.window.lift()


    def open_grades(self):
        """Otwiera okno z ocenami studenta.
        :return: """
        if self.grades_window is None or not self.grades_window.window.winfo_exists():
            self.grades_window = GradesWindow(self.user)
        else:
            self.grades_window.window.lift()

    def open_statistics(self):
        """Otwiera okno statystyk dla studenta.
        :return: """
        if self.statistics_window is None or not self.statistics_window.window.winfo_exists():
            self.statistics_window = StatisticsWindow(self.user)
        else:
            self.statistics_window.window.lift()

    # ADMIN
    def open_add_schedule(self):
        """Otwiera okno do dodawania planu zajęć (dla admina).
        :return: """
        if self.add_schedule_window is None or not self.add_schedule_window.window.winfo_exists():
            self.add_schedule_window = AddScheduleWindow(self.user)
        else:
            self.add_schedule_window.window.lift()

    def open_assign_student(self):
        """Otwiera okno przypisywania studenta do grupy (dla admina).
        :return: """
        if self.assign_student_window is None or not self.assign_student_window.window.winfo_exists():
            self.assign_student_window = AssignStudentWindow(self.user)
        else:
            self.assign_student_window.window.lift()

    def open_add_subject(self):
        """Otwiera okno dodawania przedmiotów (dla admina).
        :return: """
        if self.add_subject_window is None or not self.add_subject_window.window.winfo_exists():
            self.add_subject_window = AddSubjectWindow(self.user)
        else:
            self.add_subject_window.window.lift()

    def open_assign_teacher(self):
        """Otwiera okno przypisywania nauczyciela do przedmiotu (dla admina).
        :return: """
        if self.assign_teacher_window is None or not self.assign_teacher_window.window.winfo_exists():
            self.assign_teacher_window = AssignTeacherWindow(self.user)
        else:
            self.assign_teacher_window.window.lift()

    # TEACHER
    def open_add_grade(self):
        """Otwiera okno do dodawania ocen studentom (dla nauczycieli).
        :return: """
        if self.add_grades_window is None or not self.add_grades_window.window.winfo_exists():
            self.add_grades_window = AddGradeWindow(self.user)
        else:
            self.add_grades_window.window.lift()

    def open_schedule_teacher(self):
        """Otwiera okno z planem lekcji (dla nauczyciela).
        :return: """
        if self.schedule_window is None or not self.schedule_window.window.winfo_exists():
            self.schedule_window = TeacherScheduleWindow(self.user)
        else:
            self.schedule_window.window.lift()