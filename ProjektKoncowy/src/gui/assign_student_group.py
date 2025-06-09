import tkinter as tk
from tkinter import messagebox, ttk
from models.database import Student, Group, session


class AssignStudentWindow:
    """
       Okno służące do przypisywania studenta do wybranej grupy.
       """

    def __init__(self, user):
        """
        :param user:
        """
        self.user = user
        self.window = tk.Toplevel()
        self.window.title("Przypisz studenta do grupy")
        self.window.geometry("350x300")
        self.window.configure(bg="#fff8f0")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TLabel", font=("Helvetica", 12), background="#fff8f0",foreground="#b3541e")
        style.configure("Custom.TButton",font=("Helvetica", 12),padding=6, background="#fff8f0", foreground="#b3541e")
        style.map("Custom.TButton", background=[("active", "#f0c8a6")], foreground=[("disabled", "#a0a0a0")])
        style.configure("Custom.TMenubutton", font=("Helvetica", 12), background="#fff8f0",foreground="#b3541e",padding=6)

        # Studenci
        self.students = session.query(Student).all()
        student_names = [f"{s.first_name} {s.last_name}" for s in self.students]

        self.student_var = tk.StringVar(value=student_names[0] if student_names else "")
        self.group_var = tk.StringVar()

        tk.Label(self.window, text="Wybierz studenta:", bg="#fff8f0", font=("Helvetica", 12),
                 fg="#b3541e").pack(pady=(15, 5))
        student_menu = ttk.OptionMenu(self.window, self.student_var, self.student_var.get(), *student_names)
        student_menu.config(style="Custom.TMenubutton")
        student_menu.pack(pady=(0, 10), ipadx=10, ipady=3)

        # grupa studenta
        self.current_group_label = tk.Label(self.window, text="Aktualna grupa:", bg="#fff8f0",
                                            font=("Helvetica", 11, "italic"), fg="#555")
        self.current_group_label.pack(pady=(0, 15))

        tk.Label(self.window, text="Wybierz grupę:", bg="#fff8f0", font=("Helvetica", 12),
                 fg="#b3541e").pack(pady=(0, 5))
        self.groups = session.query(Group).all()
        group_names = [g.name for g in self.groups]
        self.group_var.set(group_names[0] if group_names else "")
        group_menu = ttk.OptionMenu(self.window, self.group_var, self.group_var.get(), *group_names)
        group_menu.config(style="Custom.TMenubutton")
        group_menu.pack(pady=(0, 15), ipadx=10, ipady=3)

        save_btn = ttk.Button(self.window, text="Zapisz", command=self.assign_to_group, style="Custom.TButton")
        save_btn.pack(pady=(5, 20), ipadx=15, ipady=5)

        # Śledzenie zmian wyboru studenta
        self.student = None
        self.student_var.trace_add("write", lambda *args: self.update_current_group_label())
        self.update_current_group_label()

    def update_current_group_label(self, event=None):
        """
        Wyświetlanie grupy dla konkretnego studenta.
        :param event:
        :return:
        """
        selected_name = self.student_var.get()
        selected_student = next((s for s in self.students if f"{s.first_name} {s.last_name}" == selected_name), None)
        if selected_student:
            self.student = selected_student
            group_name = self.student.group.name if self.student.group else "brak"
            self.current_group_label.config(text=f"Aktualna grupa: {group_name}")

    def assign_to_group(self):
        """
        Dodanie studentowi wartości gupy. Update w sqlite.
        :return:
        """
        if not self.student:
            messagebox.showerror("Błąd", "Najpierw wybierz studenta.", parent=self.window)
            return

        group_name = self.group_var.get()
        group = next((g for g in self.groups if g.name == group_name), None)

        if not group:
            messagebox.showerror("Błąd", "Nie wybrano grupy.", parent=self.window)
            return

        if self.student.group_id == group.id:
            messagebox.showinfo("Informacja", "Student już jest w tej grupie.", parent=self.window)
            return

        if len(group.students) >= group.max_students:
            messagebox.showerror("Błąd", f"Grupa '{group.name}' ma już maksymalną liczbę studentów.",parent=self.window)
            return

        self.student.group = group
        session.commit()
        messagebox.showinfo("Sukces", f"Student przypisany do grupy '{group.name}'.", parent=self.window)
        self.update_current_group_label()
