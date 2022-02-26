import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from constants import BACKGROUND, DATA_BASE, GRADE_VALUES, LABEL_FONT, PHOTO_DEFAULT, TITLE_FONT
from global_functions import add_image, run_sql, transform_image


class ViesView(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window, bg=BACKGROUND)
        self.name_database = DATA_BASE
        self.width_photo =280
        self.height_photo =140
        self.path_image = PHOTO_DEFAULT
        self.default_image = transform_image(PHOTO_DEFAULT, self.width_photo, self.height_photo)
        self.picture = self.default_image
        self.values_country = []
        self.values_city = []
        self.values_sector = []
        # Widgets
        self.title = tk.Label(self, text="Vies d'escalada", font=TITLE_FONT, bg=self.cget("bg"))
        self.frame_fields = tk.Frame(self, bg=self.cget("bg"))
        self.lb_country = tk.Label(self.frame_fields, text="País: ", font=LABEL_FONT, bg=self.cget("bg"))
        self.txt_country = ttk.Combobox(self.frame_fields, width=25)
        self.lb_city = tk.Label(self.frame_fields, text="Localitat: ", font=LABEL_FONT, bg=self.cget("bg"))
        self.txt_city = ttk.Combobox(self.frame_fields, width=25)
        self.lb_sector = tk.Label(self.frame_fields, text="Sector: ", font=LABEL_FONT, bg=self.cget("bg"))
        self.txt_sector = ttk.Combobox(self.frame_fields, width=25)
        self.lb_name = tk.Label(self.frame_fields, text="Nom via: ", font=LABEL_FONT, bg=self.cget("bg"))
        self.txt_name = tk.Entry(self.frame_fields, relief="flat", bd=0)
        self.lb_grade = tk.Label(self.frame_fields, text="Grau via: ", font=LABEL_FONT, bg=self.cget("bg"))
        self.txt_grade = ttk.Combobox(self.frame_fields, width=4, height=5, values=GRADE_VALUES)
        self.lb_comments = tk.Label(self.frame_fields, text="Comentaris: ", font=LABEL_FONT, bg=self.cget("bg"))
        self.txt_comments = tk.Text(self.frame_fields, height=8, relief="flat", bd=0)
        self.lb_img_via = tk.Label(self.frame_fields, text="Imatge via: ", font=LABEL_FONT, 
            bg=self.cget("bg"))
        self.txt_img_via = tk.Label(self.frame_fields, image=self.default_image, bg=self.cget("bg"))
        self.txt_img_via.bind("<Double Button 1>", self.add_picture)
        # Buttons
        self.frame_buttons = tk.Frame(self, bg=self.cget("bg"))
        self.bt_add = tk.Button(self.frame_buttons, text="Afegir registre", cursor="hand2", 
            command=self.add_register)
        self.bt_update = tk.Button(self.frame_buttons, text="Actualitzar registre", cursor="hand2", 
            state="disabled", command=self.update_register)
        self.bt_delete = tk.Button(self.frame_buttons, text="Eliminar registre", cursor="hand2",
            state="disabled", command=self.delete_register)
        self.bt_erase = tk.Button(self.frame_buttons, text="Esborrar camps", cursor="hand2",
            command=lambda:self.delete_fields(True))
        # Vies list
        self.frame_list = tk.Frame(self, bg=self.cget("bg"))
        self.scroll_list = ttk.Scrollbar(self.frame_list, orient="vertical")
        self.routes_list = ttk.Treeview(self.frame_list, columns=("country", "city", "sector", "name", "grade"), 
            yscrollcommand=self.scroll_list.set, height=9)
        self.routes_list.heading("#0", text="ID")
        self.routes_list.heading("country", text="País")
        self.routes_list.heading("city", text="Localitat")
        self.routes_list.heading("sector", text="Sector")
        self.routes_list.heading("name", text="Via")
        self.routes_list.heading("grade", text="Grau")
        self.routes_list.column("#0", width=56, minwidth=50, anchor="w")
        self.routes_list.column("country", width=178, minwidth=178, anchor="center")
        self.routes_list.column("city", width=178, minwidth=178, anchor="center")
        self.routes_list.column("sector", width=178, minwidth=178, anchor="center")
        self.routes_list.column("name", width=178, minwidth=178, anchor="center")
        self.routes_list.column("grade", width=50, minwidth=50, anchor="center")
        self.routes_list.bind("<Double Button 1>", self.select_routes)
        self.scroll_list.config(command=self.routes_list.yview)
        self.draw()
        self.create_table()

    def draw(self):
        self.title.pack(fill=tk.X, padx=10)
        # Data
        self.frame_fields.pack(fill=tk.X, padx=50)
        self.lb_country.grid(row=0, column=0, padx=(20, 0), pady=(10, 0), sticky="e")
        self.txt_country.grid(row=0, column=1, padx=(0, 20), pady=(10, 0))
        self.lb_city.grid(row=1, column=0, padx=(20, 0), pady=(10, 0), sticky="e")
        self.txt_city.grid(row=1, column=1, padx=(0, 20), pady=(10, 0))
        self.lb_sector.grid(row=2, column=0, padx=(20, 0), pady=(10, 0), sticky="e")
        self.txt_sector.grid(row=2, column=1, padx=(0, 20), pady=(10, 0))
        self.lb_name.grid(row=3, column=0, padx=(20, 0), pady=(10, 0), sticky="e")
        self.txt_name.grid(row=3, column=1, padx=(0, 20), pady=(10, 0), sticky="ew")
        self.lb_grade.grid(row=4, column=0, padx=(20, 0), pady=(10, 0), sticky="e")
        self.txt_grade.grid(row=4, column=1, padx=(0, 20), pady=(10, 0), sticky="w")
        self.lb_img_via.grid(row=0, column=2, pady=(10, 0), sticky="en")
        self.txt_img_via.grid(row=0, column=3, rowspan=5, padx=(0, 20), pady=(10, 0), sticky="ns")
        self.lb_comments.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="e")
        self.txt_comments.grid(row=6, column=0, columnspan=4, padx=20, pady=(0, 10), sticky="ew")
        # Buttons
        self.frame_buttons.pack(fill=tk.X, padx=50)
        self.bt_add.grid(row=0, column=0, padx=(40, 25), pady=10)
        self.bt_update.grid(row=0, column=1, padx=25, pady=10)
        self.bt_delete.grid(row=0, column=2, padx=25, pady=10)
        self.bt_erase.grid(row=0, column=3, padx=25, pady=10)
        # material list
        self.frame_list.pack(fill=tk.X)
        self.routes_list.pack(side="left", fill="both", padx=(20, 0), pady=10)
        self.scroll_list.pack(side="right", fill=tk.Y, padx=(0, 20), pady=10)

    # Buttons function
    def add_register(self):
        if self.check_fields():
            query = "INSERT INTO VIES VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
            parameters = (self.counter_ids(), self.txt_country.get().upper(), self.txt_city.get().upper(), 
                self.txt_sector.get().upper(), self.txt_name.get().upper(), self.txt_grade.get(), 
                self.path_image, self.txt_comments.get(1.0, tk.END))
            run_sql(name=self.name_database, query=query, parameters=parameters)
            messagebox.showinfo("Afegir registre", "Has afegit un registre correctament.")
            self.delete_fields()
            self.delete_routes_list()
            self.filling_routes_list()
            self.add_values()

    def update_register(self):
        if self.check_fields():
            query = "UPDATE VIES SET PAIS=?, LOCALITAT=?, SECTOR=?, NOM=?, GRAU=?, FOTO=?, COMENTARIS=? WHERE ID=?"
            parameters = (self.txt_country.get().upper(), self.txt_city.get().upper(), 
                self.txt_sector.get().upper(), self.txt_name.get().upper(), self.txt_grade.get(), 
                self.path_image, self.txt_comments.get(1.0, tk.END), 
                self.routes_list.item(self.routes_list.selection()[0], "text"))
            run_sql(name=self.name_database, query=query, parameters=parameters)
            messagebox.showinfo("Actualitzar registre", "Has actualitzat un registre correctament.")
            self.delete_fields()
            self.delete_routes_list()
            self.filling_routes_list()
            self.add_values()

    def delete_register(self):
        option = messagebox.askokcancel("Eliminar registre", "Estas segur d'eliminar el registre?")
        if option:
            query = "DELETE FROM VIES WHERE ID=?"
            param = (self.routes_list.item(self.routes_list.selection()[0], "text"), )
            run_sql(name=self.name_database, query=query, parameters=param)
            messagebox.showinfo("Eliminar registre", "Has eliminat un registre correctament.")
            self.delete_fields()
            self.delete_routes_list()
            self.filling_routes_list()
            self.add_values()

    def delete_fields(self, button=False):
        self.txt_country.delete(0, tk.END)
        self.txt_city.delete(0, tk.END)
        self.txt_sector.delete(0, tk.END)
        self.txt_name.delete(0, tk.END)
        self.txt_grade.delete(0, tk.END)
        self.txt_comments.delete(1.0, tk.END)
        self.txt_img_via["image"] = self.default_image
        self.txt_country.focus()
        self.bt_update["state"] = "disabled"
        self.bt_delete["state"] = "disabled"
        if button:
            self.routes_list.selection_remove(self.routes_list.selection())

    # functions
    def select_routes(self, event):
        paramenter = (self.routes_list.item(self.routes_list.selection()[0], "text"), )
        query = "SELECT * FROM VIES WHERE ID=?"
        data = run_sql(name=self.name_database, query=query, parameters=paramenter, read=True)
        for item in data:
            self.delete_fields()
            self.txt_country.insert(0, item[1])
            self.txt_city.insert(0, item[2])
            self.txt_sector.insert(0, item[3])
            self.txt_name.insert(0, item[4])
            self.txt_grade.insert(0, item[5])
            self.picture = transform_image(item[6], self.width_photo, self.height_photo)
            self.txt_comments.insert(1.0, item[7])
            self.bt_update["state"] = "normal"
            self.bt_delete["state"] = "normal"

    def add_picture(self, event):
        self.path_image = add_image()
        if self.path_image:
            self.picture = transform_image(self.path_image, self.width_photo, self.height_photo)
            self.txt_img_via["image"] = self.picture

    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS VIES (ID INTEGER PRIMARY KEY, PAIS TEXT, LOCALITAT TEXT, 
        SECTOR TEXT, NOM TEXT, GRAU TEXT, FOTO TEXT, COMENTARIS TEXT)"""
        run_sql(name=self.name_database, query=query)
        self.delete_routes_list()
        self.filling_routes_list()

    def counter_ids(self):
        count = 1
        query = "SELECT ID FROM VIES ORDER BY ID"
        data = run_sql(name=self.name_database, query=query, read=True)
        for item in data:
            if item[0] != count:
                break
            count += 1
        return count
        self.add_values()

    def check_fields(self):
        if self.txt_country.get() != "" and self.txt_city.get() != "" and self.txt_sector.get() and self.txt_name.get() != "":
            return True
        else:
            messagebox.showerror("Error", "Has d'incerir el país, la localitat, el sector i el nom de la via.")
            return False

    def delete_routes_list(self):
        for item in self.routes_list.get_children():
            self.routes_list.delete(item)

    def filling_routes_list(self):
        query = "SELECT ID, PAIS, LOCALITAT, SECTOR, NOM, GRAU FROM VIES ORDER BY ID"
        data = run_sql(name=self.name_database, query=query, read=True)
        for item in data:
            text = item[0]
            values = (item[1], item[2], item[3], item[4], item[5])
            self.routes_list.insert("", tk.END, text=text, values=values)

    def add_values(self):
        query = "SELECT PAIS, LOCALITAT, SECTOR FROM VIES ORDER BY PAIS, LOCALITAT, SECTOR"
        data = run_sql(name=self.name_database, query=query, read=True)
        for item in data:
            if item[0] not in self.values_country:
                self.values_country.append(item[0])
            if item[1] not in self.values_city:
                self.values_city.append(item[1])
            if item[2] not in self.values_sector:
                self.values_sector.append(item[2])
        self.txt_country["values"] = self.values_country
        self.txt_city["values"] = self.values_city
        self.txt_sector["values"] = self.values_sector