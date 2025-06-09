import tkinter as tk
from tkinter import messagebox, ttk
from models.database import Teacher, Subject, session

class AssignTeacherWindow:
    """
       Okno umożliwiające przypisanie wybranego przedmiotu do nauczyciela.
       """

    def __init__(self, user):
        """
        :param user:
        """
        self.user = user
        self.window = tk.Toplevel()
        self.window.title("Przypisz przedmiot nauczycielowi")
        self.window.geometry("350x280")
        self.window.configure(bg="#fff8f0")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TLabel", font=("Helvetica", 12), background="#fff8f0", foreground="#b3541e")
        style.configure("Custom.TButton", font=("Helvetica", 12), padding=6, background="#fff8f0", foreground="#b3541e")
        style.map("Custom.TButton", background=[("active", "#f0c8a6")], foreground=[("disabled", "#a0a0a0")])
        style.configure("Custom.TMenubutton", font=("Helvetica", 12), background="#fff8f0", foreground="#b3541e",
                        padding=6)

        # nauczyciele
        self.teachers = session.query(Teacher).all()
        teacher_names = [f"{t.first_name} {t.last_name}" for t in self.teachers]
        self.teacher_var = tk.StringVar(value=teacher_names[0] if teacher_names else "")

        ttk.Label(self.window, text="Wybierz nauczyciela:", style="Custom.TLabel").pack(pady=(20, 5))
        teacher_menu = ttk.OptionMenu(self.window, self.teacher_var, self.teacher_var.get(), *teacher_names)
        teacher_menu.config(style="Custom.TMenubutton")
        teacher_menu.pack(pady=(0, 15), ipadx=10, ipady=3)

        # lista przedmiotów
        self.subjects = session.query(Subject).all()
        subject_names = [f"{s.name} ({s.nick})" for s in self.subjects]
        self.subject_var = tk.StringVar(value=subject_names[0] if subject_names else "")

        ttk.Label(self.window, text="Wybierz przedmiot:", style="Custom.TLabel").pack(pady=(0, 5))
        subject_menu = ttk.OptionMenu(self.window, self.subject_var, self.subject_var.get(), *subject_names)
        subject_menu.config(style="Custom.TMenubutton")
        subject_menu.pack(pady=(0, 20), ipadx=10, ipady=3)

        assign_btn = ttk.Button(self.window, text="Przypisz", command=self.assign_subject_to_teacher,
                                style="Custom.TButton")
        assign_btn.pack(pady=(0, 20), ipadx=15, ipady=5)

    def assign_subject_to_teacher(self):
        """
        Dodanie w bd nowej instarcji do tabeli teacher-subject.
        :return:
        """
        selected_teacher_name = self.teacher_var.get()
        teacher = next((t for t in self.teachers if f"{t.first_name} {t.last_name}" == selected_teacher_name), None)

        selected_subject_name = self.subject_var.get()
        subject = next((s for s in self.subjects if f"{s.name} ({s.nick})" == selected_subject_name), None)

        if not teacher or not subject:
            messagebox.showerror("Błąd", "Nie wybrano nauczyciela lub przedmiotu.", parent=self.window)
            return

        if subject in teacher.subjects:
            messagebox.showinfo("Informacja", "Ten nauczyciel już prowadzi ten przedmiot.", parent=self.window)
            return

        teacher.subjects.append(subject)
        session.commit()
        messagebox.showinfo("Sukces",f"Przypisano przedmiot '{subject.name}' do nauczyciela '{teacher.first_name} {teacher.last_name}'.",parent=self.window)