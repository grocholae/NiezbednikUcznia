import tkinter as tk
from gui.login_window import LoginWindow
from models.database import init_db

if __name__ == "__main__":
    """
     Wywołanie całego programu oraz wyświetlenie GUI.
    """
    init_db()
    root = tk.Tk()
    root.title("Niezbędnik Ucznia")
    root.geometry("800x800")
    app = LoginWindow(root)
    root.mainloop()