from tkinter import messagebox

from fpdf import FPDF
import os
from models.database import session, Time, Schedule, Student, Subject, Group

class PDF(FPDF):
    """
        Służy do eksportu ocen i planu do plików pdf, które są zapisywane w folderze raporty.
    """
    def header(self):
        self.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        self.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf', uni=True)
        self.set_font("DejaVu", 'B', 14)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, "Niezbędnik Ucznia", ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", 'B', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Strona {self.page_no()}', align='C')



def export_schedule(student):
    """
            Eksport planu studenta w estetyczne sposób z wyciąganiem danych z bazy danych.
        """
    days_of_week = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
    pdf = PDF("L", "mm", "A4")
    pdf.add_page()
    pdf.set_font("DejaVu", 'B', 12)
    pdf.cell(0, 10, "Plan zajęć", ln=True)
    pdf.ln(5)

    pdf.set_text_color(	25 ,25 ,112)


    times = session.query(Time).order_by(Time.id).all()
    schedule_map = {
        day: {time.id: None for time in times}
        for day in days_of_week
    }

    for s in student.schedules:

        if s.day in schedule_map:
            schedule_map[s.day][s.time_id] = (s.subject.nick, f"{s.teacher.first_name} {s.teacher.last_name}",s.subject.color)



    cell_width = 50
    time_width = 25
    row_height = 20

    # Nagłówki kolumn
    pdf.set_font("DejaVu", 'B', 10)
    pdf.cell(time_width, row_height, "Godzina", border=1, align='C')
    for day in days_of_week:
        pdf.cell(cell_width, row_height, day, border=1, align='C')
    pdf.ln()

    pdf.set_text_color(0,0,0)
    pdf.set_font("DejaVu", '', 9)
    for time in times:
        pdf.cell(time_width, row_height / 2, time.time, border='LTR', align='C')
        #górna część
        for day in days_of_week:
            entry = schedule_map[day][time.id]
            if entry:
                subject_nick, _, color = entry
                r, g, b = hex_to_rgb(color)
                pdf.set_fill_color(r, g, b)
                pdf.cell(cell_width, row_height / 2, subject_nick, border='LTR', align='C', fill=True)
            else:
                pdf.cell(cell_width, row_height / 2, "", border='LTR')

        pdf.ln()

        # dolna część
        pdf.cell(time_width, row_height / 2, "", border='LRB')  # dolna część godziny (pusta)

        for day in days_of_week:
            entry = schedule_map[day][time.id]
            if entry:
                _, teacher_name, color = entry
                r, g, b = hex_to_rgb(color)
                pdf.set_fill_color(r, g, b)
                pdf.cell(cell_width, row_height / 2, teacher_name, border='LRB', align='C', fill=True)
            else:
                pdf.cell(cell_width, row_height / 2, "", border='LRB')

        pdf.ln()

    # Nazwa pliku (użyj swojej funkcji sanitize_filename_component)
    filename = f"plan_id{student.id}_{sanitize_filename_component(student.first_name)}_{sanitize_filename_component(student.last_name)}.pdf"
    os.makedirs("raporty", exist_ok=True)
    pdf.output(os.path.join("raporty", filename))
    messagebox.showinfo("Eksport", f"Plan lekcji zapisano do pliku:\n{filename}")

def hex_to_rgb(hex_color):
    """
     Konwertuje kolor w formacie szesnastkowym (#RRGGBB) na krotkę RGB.

    :param hex_color: Kolor w formacie heksadecymalnym (np. "#FFFFFF").
    :type hex_color: str
    :return: Krotka z wartościami (R, G, B).
    :rtype: tuple(int, int, int)
    """
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def export_grades(user):
    """
                Eksport ocen studenta w estetyczne sposób z wyciąganiem danych z bazy danych.
            """
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("DejaVu", 'B', 12)
    pdf.cell(0, 10, "Oceny", ln=True)
    pdf.ln(5)

    pdf.set_font("DejaVu", 'B', 11)
    pdf.cell(60, 10, "Przedmiot", border=1)
    pdf.cell(30, 10, "Ocena", border=1)
    pdf.cell(40, 10, "Data", border=1)
    pdf.ln()

    pdf.set_font("DejaVu", '', 11)
    for g in user.grades:
        pdf.cell(60, 10, str(g.subject.name), border=1)
        pdf.cell(30, 10, str(g.grade), border=1)
        pdf.cell(40, 10, str(g.date), border=1)
        pdf.ln()

    filename = f"oceny_id{user.id}_{sanitize_filename_component(user.first_name)}_{sanitize_filename_component(user.last_name)}.pdf"
    os.makedirs("raporty", exist_ok=True)
    pdf.output(os.path.join("raporty", filename))
    messagebox.showinfo("Eksport", f"Oceny zapisano do pliku:\n{filename}")

def sanitize_filename_component(s):
    """
              Zmiana zapisu pełnej ścieżki.
            """
    return str(s).replace(" ", "_").replace("/", "_")



def export_schedule_teacher(teacher):
    """
                Eksport planu nauczyciela w estetyczne sposób z wyciąganiem danych z bazy danych.
            """
    days_of_week = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
    pdf = PDF("L", "mm", "A4")
    pdf.add_page()
    pdf.set_font("DejaVu", 'B', 12)
    pdf.cell(0, 10, "Plan zajęć", ln=True)
    pdf.ln(5)

    pdf.set_text_color(	25 ,25 ,112)


    times = session.query(Time).order_by(Time.id).all()
    schedule_map = {
        day: {time.id: None for time in times}
        for day in days_of_week
    }

    entries = (
        session.query(Schedule.day, Schedule.time_id, Schedule.subject_id, Student.group_id)
        .join(Student, Schedule.student_id == Student.id)
        .filter(Schedule.teacher_id == teacher.id)
        .distinct()
        .all()
    )

    for day, time_id, subject_id, group_id in entries:
        subject = session.query(Subject).get(subject_id)
        group = session.query(Group).get(group_id)
        if day in schedule_map:
            schedule_map[day][time_id] = (subject.nick, group.name, subject.color)



    cell_width = 50
    time_width = 25
    row_height = 20

    # Nagłówki kolumn
    pdf.set_font("DejaVu", 'B', 10)
    pdf.cell(time_width, row_height, "Godzina", border=1, align='C')
    for day in days_of_week:
        pdf.cell(cell_width, row_height, day, border=1, align='C')
    pdf.ln()

    pdf.set_text_color(0,0,0)
    pdf.set_font("DejaVu", '', 9)
    for time in times:
        pdf.cell(time_width, row_height / 2, time.time, border='LTR', align='C')
        #górna część
        for day in days_of_week:
            entry = schedule_map[day][time.id]
            if entry:
                subject_nick, _, color = entry
                r, g, b = hex_to_rgb(color)
                pdf.set_fill_color(r, g, b)
                pdf.cell(cell_width, row_height / 2, subject_nick, border='LTR', align='C', fill=True)
            else:
                pdf.cell(cell_width, row_height / 2, "", border='LTR')

        pdf.ln()

        # dolna część
        pdf.cell(time_width, row_height / 2, "", border='LRB')  # dolna część godziny (pusta)

        for day in days_of_week:
            entry = schedule_map[day][time.id]
            if entry:
                _, group_name, color = entry
                r, g, b = hex_to_rgb(color)
                pdf.set_fill_color(r, g, b)
                pdf.cell(cell_width, row_height / 2, group_name, border='LRB', align='C', fill=True)
            else:
                pdf.cell(cell_width, row_height / 2, "", border='LRB')

        pdf.ln()

    # Nazwa pliku (użyj swojej funkcji sanitize_filename_component)
    filename = f"plan_t_id{teacher.id}_{sanitize_filename_component(teacher.first_name)}_{sanitize_filename_component(teacher.last_name)}.pdf"
    os.makedirs("raporty", exist_ok=True)
    pdf.output(os.path.join("raporty", filename))
    messagebox.showinfo("Eksport", f"Plan zajęć zapisano do pliku:\n{filename}")