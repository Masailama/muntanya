import tkinter as tk
from constants import BACKGROUND, LABEL_FONT, TITLE_FONT
from material import MaterialView
from vies_escalada import ViesView


class Menu(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window, bg=BACKGROUND)
        self.window = window
        self.option = 0     # 0:menu, 1:material, 2:vies
        self.title = tk.Label(self, text="Menu muntanya", font=TITLE_FONT, bg=self.cget("bg"))
        self.bt_material = tk.Button(self, text="Material muntanya", font=LABEL_FONT, cursor="hand2", 
            command=self.option_material)
        self.bt_vies = tk.Button(self, text="Vies d'escalada", font=LABEL_FONT, cursor="hand2", 
            command=self.option_vies)
        self.material = MaterialView(self.window)
        self.vies = ViesView(self.window)
        self.bt_back = tk.Label(self.window, text="<< Menu", font=LABEL_FONT, bg=self.window.cget("bg"), 
            anchor="w", cursor="hand2")
        self.bt_back.bind("<Button 1>", self.option_back)
        self.draw()

    def draw(self):
        self.pack(fill="both", padx=20, pady=20)
        self.title.pack(fill=tk.X, padx=20, pady=20, ipadx=10)
        self.bt_material.pack(fill=tk.X, padx=20, pady=(10, 0))
        self.bt_vies.pack(fill=tk.X, padx=20, pady=(10, 20))

    def option_material(self):
        self.pack_forget()
        self.bt_back.pack(fill=tk.X)
        self.material.pack(fill="both", expand=1, padx=10, pady=(0, 20))
        self.option = 1

    def option_vies(self):
        self.pack_forget()
        self.bt_back.pack(fill=tk.X)
        self.vies.pack(fill="both", expand=1, padx=10, pady=(0, 20))
        self.option = 2

    def option_back(self, event):
        if self.option == 1:
            self.material.pack_forget()
            self.pack(fill="both", padx=20, pady=20)
            self.option = 0
        elif self.option == 2:
            self.vies.pack_forget()
            self.pack(fill="both", padx=20, pady=20)
            self.option = 0
        self.bt_back.pack_forget()