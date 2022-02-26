import tkinter as tk
from menu import Menu


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Muntanya")
        self.resizable(0, 0)
        self.config(bg="white")
        self.geometry("+200+0")


if __name__ =="__main__":
    app = App()
    menu = Menu(app)
    app.mainloop()