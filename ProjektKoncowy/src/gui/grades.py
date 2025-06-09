import tkinter as tk
from models.database import session, Grade
from utils.pdf_export import export_grades



class GradesWindow:
    """
     Student po wejściu w dziennik ocen dostaje informacje na temat historii wszystkich ocen oraz może je wyeksportować do pdf.
    """
    def __init__(self, user):
        """
        :param user:
        """
        self.user = user
        self.window = tk.Toplevel()
        self.window.title("Dziennik ocen")
        self.window.geometry("800x400")
        self.window.minsize(700, 300)
        self.window.configure(bg="#fff8f0")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)

        title_lbl = tk.Label(self.window, text="Historia ocen", font=("Helvetica", 18, "bold"), bg="#fff8f0", fg="#b3541e")
        title_lbl.grid(row=0, column=0, pady=(15, 5), sticky="n")

        self.columns = ["Ocena", "Przedmiot", "Nauczyciel", "Data Wystawienia"]
        self.grades = session.query(Grade).filter_by(student_id=self.user.id).all()
        self.grid_frame = tk.Frame(self.window, bg="#fff8f0")
        self.grid_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)

        #for col in range(len(self.columns) + 1):
        #    self.grid_frame.grid_columnconfigure(col, minsize=200, weight=1, uniform="grade_col")
        self.grid_frame.grid_columnconfigure(0, minsize=40, weight=1)  # Lp.
        self.grid_frame.grid_columnconfigure(1, minsize=80, weight=1)  # Ocena
        self.grid_frame.grid_columnconfigure(2, minsize=200, weight=4)  # Przedmiot
        self.grid_frame.grid_columnconfigure(3, minsize=150, weight=3)  # Nauczyciel
        self.grid_frame.grid_columnconfigure(4, minsize=100, weight=2)  # Data

        self.build_grade_grid()

        btn_frame = tk.Frame(self.window, bg="#fff8f0")
        btn_frame.grid(row=2, column=0, pady=(0, 15))
        export_btn = tk.Button(btn_frame, text="Eksportuj do PDF", command=self.export,
                               bg="#d0a96f", fg="white", font=("Helvetica", 12, "bold"), relief="raised", padx=10,pady=5)
        export_btn.pack(pady=(10, 0))

    def build_grade_grid(self):
        """
        Wyrysowanie w GUI ocen studenta oraz wyciągnięcie ich z bd.
        :return:
        """
        header_font = ("Helvetica", 12, "bold")
        cell_font = ("Helvetica", 11)
        header_bg = "#f5c6aa"
        cell_bg = "#fff1e6"
        alt_cell_bg = "#ffe8d6"

        for col, column_name in enumerate(["Lp."] + self.columns):
            lbl = tk.Label(self.grid_frame, text=column_name, font=header_font, bg=header_bg,
                           borderwidth=1, relief="solid")
            lbl.grid(row=0, column=col, sticky="nsew")

        for row, grade in enumerate(self.grades, start=1):
            bg_color = cell_bg if row % 2 == 1 else alt_cell_bg
            # Lp.
            tk.Label(self.grid_frame, text=str(row), font=cell_font, bg=bg_color,
                     borderwidth=1, relief="solid").grid(row=row, column=0, sticky="nsew")
            # Ocena
            tk.Label(self.grid_frame, text=str(grade.grade), font=cell_font, bg=bg_color,
                     borderwidth=1, relief="solid").grid(row=row, column=1, sticky="nsew")
            # Przedmiot
            tk.Label(self.grid_frame, text=str(grade.subject.name), font=cell_font, bg=bg_color,
                     borderwidth=1, relief="solid").grid(row=row, column=2, sticky="nsew")
            # Nauczyciel
            teacher_name = f"{grade.teacher.first_name} {grade.teacher.last_name}" if hasattr(grade, 'teacher') and grade.teacher else "-"
            tk.Label(self.grid_frame, text=teacher_name, font=cell_font, bg=bg_color,
                     borderwidth=1, relief="solid").grid(row=row, column=3, sticky="nsew")
            # Data wystawienia
            date_str = grade.date
            tk.Label(self.grid_frame, text=date_str, font=cell_font, bg=bg_color,
                     borderwidth=1, relief="solid").grid(row=row, column=4, sticky="nsew")

    def export(self):
        """
        Wywołuje metodę odpowiedzialną za eksport do PDF ocen studenta.
        :return:
        """
        export_grades(self.user)