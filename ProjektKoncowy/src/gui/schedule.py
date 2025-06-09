import tkinter as tk
from models.database import session, Schedule, Time
from utils.pdf_export import export_schedule


class ScheduleWindow:
    """
    Wyświelta dla użytkownika - studenta plan jego zajęć wraz z możliwością eksportu planu do pdf.
    """

    def __init__(self, user):
        """
        :param user:
        """
        self.student = user
        self.days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
        self.times = session.query(Time).all()
        self.window = tk.Toplevel()
        self.window.title(f"Plan lekcji")
        self.window.configure(bg="#fff8f0")
        self.window.minsize(600, 500)
        self.main_frame = tk.Frame(self.window, bg="#fff8f0")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.grid_frame = tk.Frame(self.main_frame, bg="#fff8f0")
        self.grid_frame.pack()
        if not user.group:
            tk.Label(
                self.main_frame,
                text="Brak planu lekcji do wyświetlenia.",
                font=("Helvetica", 12),
                fg="gray",
                bg="#fff8f0",
            ).pack()
        else:
            self.build_schedule_grid()

        export_btn = tk.Button(
            self.main_frame,
            text="Eksportuj do PDF",
            command=self.export,
            bg="#d0a96f",
            fg="white",
            font=("Helvetica", 12, "bold"),
            relief="raised",
            padx=10,
            pady=5,
        )
        export_btn.pack(pady=15)

    def build_schedule_grid(self):
        """
        Wyrysowanie planu zajęć.
        :return:
        """
        for col in range(len(self.days) + 1):
            self.grid_frame.grid_columnconfigure(col, minsize=160)

        for col, day in enumerate([""] + self.days):
            tk.Label(
                self.grid_frame,
                text=day,
                borderwidth=1,
                relief="solid",
                width=20,
                bg="#d9d9d9",
                font=("Helvetica", 11, "bold"),
            ).grid(row=0, column=col, sticky="nsew")

        for row, time in enumerate(self.times, start=1):
            tk.Label(
                self.grid_frame,
                text=time.time,
                borderwidth=1,
                relief="solid",
                width=20,
                bg="#bde0fe",
                font=("Helvetica", 10),
            ).grid(row=row, column=0, sticky="nsew")

            for col, day in enumerate(self.days, start=1):
                schedule = (
                    session.query(Schedule)
                    .filter_by(student_id=self.student.id, day=day, time_id=time.id)
                    .first()
                )

                if schedule:
                    subject_name = schedule.subject.name
                    teacher_name = f"{schedule.teacher.first_name} {schedule.teacher.last_name}"
                    text = f"{subject_name}\n{teacher_name}"
                    color = schedule.subject.color
                else:
                    text = ""
                    color = "#FFFFFF"

                tk.Label(
                    self.grid_frame,
                    text=text,
                    borderwidth=1,
                    relief="solid",
                    width=20,
                    height=4,
                    font=("Helvetica", 10),
                    bg=color,
                    wraplength=150,
                    justify="center",
                ).grid(row=row, column=col, sticky="nsew")

    def export(self):
        """
         Eksport do PDF. Wywyołanie metody z utils/pdf_export.py
        :return:
        """
        export_schedule(self.student)
