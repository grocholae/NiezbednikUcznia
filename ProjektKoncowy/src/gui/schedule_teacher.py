import tkinter as tk
from models.database import session, Schedule, Time, Student, Subject, Group
from utils.pdf_export import export_schedule_teacher


class TeacherScheduleWindow:
    """
    Wyświetla dla nauczyciela plan jego zajęć wraz z możliwością eksportu planu do PDF.
    """
    def __init__(self, teacher):
        """
        :param teacher:
        """
        self.teacher = teacher
        self.days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
        self.times = session.query(Time).all()
        self.window = tk.Toplevel()
        self.window.title(f"Plan zajęć")
        self.window.configure(bg="#fff8f0")
        self.window.minsize(600, 500)

        self.main_frame = tk.Frame(self.window, bg="#fff8f0")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.grid_frame = tk.Frame(self.main_frame, bg="#fff8f0")
        self.grid_frame.pack()

        if not self.has_schedule():
            tk.Label(self.main_frame, text="Brak planu zajęć do wyświetlenia.", font=("Helvetica", 12), fg="gray", bg="#fff8f0").pack()
        else:
            self.build_schedule_grid()

        export_btn = tk.Button(self.main_frame, text="Eksportuj do PDF", command=self.export, bg="#d0a96f", fg="white", font=("Helvetica", 12, "bold"), relief="raised", padx=10, pady=5)
        export_btn.pack(pady=15)

    def has_schedule(self):
        """
        Sprawdzenie czy ma plan zajęć w bd - sqlite.
        :return:
        """
        return session.query(Schedule).filter_by(teacher_id=self.teacher.id).first() is not None

    def build_schedule_grid(self):
        """
        Wyrysowanie planu zajęć.
        :return:
        """
        schedule_entries = (
            session.query(Schedule.day, Schedule.time_id, Schedule.subject_id, Student.group_id)
            .join(Student, Schedule.student_id == Student.id)
            .filter(Schedule.teacher_id == self.teacher.id)
            .distinct()
            .all()
        )
        # Mapa: (day, time_id) -> (subject_name, group_name, color)
        schedule_map = {}
        for day, time_id, subject_id, group_id in schedule_entries:
            subject = session.query(Subject).get(subject_id)
            group = session.query(Group).get(group_id)
            schedule_map[(day, time_id)] = (subject.name, group.name, subject.color)


        for col in range(len(self.days) + 1):
            self.grid_frame.grid_columnconfigure(col, minsize=160)

        for col, day in enumerate([""] + self.days):
            tk.Label(self.grid_frame, text=day, borderwidth=1, relief="solid", width=20, bg="#d9d9d9",
                     font=("Helvetica", 11, "bold")
                     ).grid(row=0, column=col, sticky="nsew")

        for row, time in enumerate(self.times, start=1):
            tk.Label(self.grid_frame, text=time.time, borderwidth=1, relief="solid", width=20, bg="#bde0fe",
                     font=("Helvetica", 10)
                     ).grid(row=row, column=0, sticky="nsew")

            for col, day in enumerate(self.days, start=1):
                key = (day, time.id)
                entry = schedule_map.get(key)

                if entry:
                    subject_name, group_name, color = entry
                    text = f"{subject_name}\n{group_name}"
                else:
                    text = ""
                    color = "#FFFFFF"

                tk.Label(self.grid_frame, text=text, borderwidth=1, relief="solid", width=20, height=4,
                         font=("Helvetica", 10), bg=color, wraplength=150, justify="center"
                         ).grid(row=row, column=col, sticky="nsew")

    def export(self):
        """
        Eksport do PDF. Wywyołanie metody z utils/pdf_export.py
        :return:
        """
        export_schedule_teacher(self.teacher)