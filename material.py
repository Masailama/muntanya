import tkinter as tk
from tkinter import ttk, messagebox
from constants import BACKGROUND, DATA_BASE, LABEL_FONT, PHOTO_DEFAULT, TITLE_FONT
from global_functions import add_image, run_sql, transform_image


class MaterialView(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window, bg=BACKGROUND)
        self.type_values = []   # valors que apareixen al combobox type
        self.mark_values = []   # valors que apareixen al combobox mark
        self.name_database = DATA_BASE
        self.width_photo = 120
        self.height_photo = 120
        self.path_img = PHOTO_DEFAULT
        self.default_img = transform_image(PHOTO_DEFAULT, self.width_photo, self.height_photo)
        self.img_photo = self.default_img
        # Widgets
        self.title = tk.Label(self, text="Material d'escalada", font=TITLE_FONT, bg=self.cget("bg"))
        self.frame_data = tk.Frame(self, bg=self.cget("bg"))
        self.lb_type = tk.Label(self.frame_data, text="Tipus: ", font=LABEL_FONT, bg=self.cget("bg"))
        self.txt_type = ttk.Combobox(self.frame_data, width=25)
        self.lb_mark = tk.Label(self.frame_data, text="Marca: ", font=LABEL_FONT, bg=self.cget("bg"))
        self.txt_mark = ttk.Combobox(self.frame_data, width=25)
        self.lb_model = tk.Label(self.frame_data, text="Model: ", font=LABEL_FONT, bg=self.cget("bg"))
        self.txt_model = tk.Entry(self.frame_data, width=27, relief="flat", bd=0)
        self.lb_photo = tk.Label(self.frame_data, text="Fotografía: ", font=LABEL_FONT, bg=self.cget("bg"))
        self.txt_photo = tk.Label(self.frame_data, image=self.default_img)
        self.txt_photo.bind("<Double Button 1>", self.add_images)
        self.lb_comments = tk.Label(self.frame_data, text="Observacions: ", font=LABEL_FONT, bg=self.cget("bg"))
        self.txt_comments = tk.Text(self.frame_data, relief="flat", bd=0, height=5, width=75)
        self.frame_buttons = tk.Frame(self, bg=self.cget("bg"))
        self.bt_add = tk.Button(self.frame_buttons, text="Afegir registre", cursor="hand2", 
            command=self.add_register)
        self.bt_update = tk.Button(self.frame_buttons, text="Actualitzar registre", cursor="hand2", 
            state="disabled", command=self.update_register)
        self.bt_delete = tk.Button(self.frame_buttons, text="Eliminar registre", cursor="hand2",
            state="disabled", command=self.delete_register)
        self.bt_erase = tk.Button(self.frame_buttons, text="Esborrar camps", cursor="hand2",
            command=lambda:self.delete_fields(True))
        self.frame_list = tk.Frame(self, bg=self.cget("bg"))
        self.scroll_list = ttk.Scrollbar(self.frame_list, orient="vertical")
        self.material_list = ttk.Treeview(self.frame_list, columns=("type", "mark", "model"), 
            yscrollcommand=self.scroll_list.set)
        self.material_list.heading("#0", text="ID")
        self.material_list.heading("type", text="Tipus")
        self.material_list.heading("mark", text="Marca")
        self.material_list.heading("model", text="Model")
        self.material_list.column("#0", width=56, minwidth=50, anchor="w")
        self.material_list.column("type", width=178, minwidth=178, anchor="center")
        self.material_list.column("mark", width=178, minwidth=178, anchor="center")
        self.material_list.column("model", width=178, minwidth=178, anchor="center")
        self.material_list.bind("<Double Button 1>", self.select_material)
        self.scroll_list.config(command=self.material_list.yview)
        self.draw()
        self.create_table()

    def draw(self):
        self.title.pack(fill=tk.X, padx=10)
        # data
        self.frame_data.pack(fill=tk.X)
        self.lb_type.grid(row=0, column=0, padx=(20, 0), pady=(10, 0), sticky="e")
        self.txt_type.grid(row=0, column=1, padx=(0, 10), pady=(10, 0))
        self.lb_mark.grid(row=1, column=0, padx=(20, 0), pady=(10, 0), sticky="e")
        self.txt_mark.grid(row=1, column=1, padx=(0, 10), pady=(10, 0))
        self.lb_model.grid(row=2, column=0, padx=(20, 0), pady=(10, 0), sticky="e")
        self.txt_model.grid(row=2, column=1, padx=(0, 10), pady=(10, 0))
        self.lb_photo.grid(row=0, column=2, padx=(100, 0), pady=(10, 0))
        self.txt_photo.grid(row=0, column=3, rowspan=4, padx=(0, 20), pady=(10, 0))
        self.lb_comments.grid(row=3, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="w")
        self.txt_comments.grid(row=4, column=0, columnspan=4, padx=10, pady=(0, 10))
        # buttons
        self.frame_buttons.pack(fill=tk.X)
        self.bt_add.grid(row=0, column=0, padx=(25, 10), pady=10)
        self.bt_update.grid(row=0, column=1, padx=10, pady=10)
        self.bt_delete.grid(row=0, column=2, padx=10, pady=10)
        self.bt_erase.grid(row=0, column=3, padx=(10, 20), pady=10)
        # material list
        self.frame_list.pack(fill=tk.X)
        self.material_list.pack(side="left", fill="both", padx=(20, 0), pady=10)
        self.scroll_list.pack(side="right", fill=tk.Y, padx=(0, 20), pady=10)

    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS MATERIAL (ID INTEGER PRIMARY KEY, TIPUS TEXT, MARCA TEXT,
        MODEL TEXT, FOTO TEXT, COMENTARIS TEXT)"""
        run_sql(self.name_database, query)
        self.counter_ids()
        self.delete_material_list()
        self.filling_material_list()
        self.add_values()

    def check_fields(self):
        if self.txt_type.get() != "" and self.txt_mark.get() != "" and self.txt_model.get() != "":
            return True
        else:
            messagebox.showerror("Error", "Has d'incerir el tipus, la marca i el model obligatoriament.")
            return False

    def counter_ids(self):
        count = 1
        query = "SELECT ID FROM MATERIAL ORDER BY ID"
        data = run_sql(name=self.name_database, query=query, read=True)
        for item in data:
            if item[0] != count:
                break
            count += 1
        return count

    def filling_material_list(self):
        query = "SELECT ID, TIPUS, MARCA, MODEL FROM MATERIAL ORDER BY ID"
        data = run_sql(name=self.name_database, query=query, read=True)
        for item in data:
            text = item[0]
            values = (item[1], item[2], item[3])
            self.material_list.insert("", tk.END, text=text, values=values)

    def delete_material_list(self):
        for item in self.material_list.get_children():
            self.material_list.delete(item)

    def add_values(self):
        query = "SELECT TIPUS, MARCA FROM MATERIAL ORDER BY TIPUS, MARCA"
        data = run_sql(name=self.name_database, query=query, read=True)
        for item in data:
            if item[0] not in self.type_values:
                self.type_values.append(item[0])
            if item[1] not in self.mark_values:
                self.mark_values.append(item[1])
        self.txt_type["values"] = self.type_values
        self.txt_mark["values"] = self.mark_values
        
    def add_images(self, event):
        self.path_img = add_image()
        if self.path_img:    
            self.img_photo = transform_image(self.path_img, self.width_photo, self.height_photo)
            self.txt_photo["image"] = self.img_photo

    def select_material(self, event):
        parameter = (self.material_list.item(self.material_list.selection()[0], "text"), )
        query = "SELECT * FROM MATERIAL WHERE ID=?"
        data = run_sql(name=self.name_database, query=query, parameters=parameter, read=True)
        for item in data:
            self.delete_fields()
            self.txt_type.insert(0, item[1])
            self.txt_mark.insert(0, item[2])
            self.txt_model.insert(0, item[3])
            self.path_img = item[4]
            self.img_photo = transform_image(self.path_img, self.width_photo, self.height_photo)
            self.txt_photo["image"] = self.img_photo
            self.txt_comments.insert(1.0, item[5])
            self.bt_update["state"] = "normal"
            self.bt_delete["state"] = "normal"

    # buttons functions
    def delete_fields(self, button=False):
        self.txt_type.delete(0, tk.END)
        self.txt_mark.delete(0, tk.END)
        self.txt_model.delete(0, tk.END)
        self.txt_comments.delete(1.0, tk.END)
        self.txt_photo["image"] = self.default_img
        self.txt_type.focus()
        self.bt_update["state"] = "disabled"
        self.bt_delete["state"] = "disabled"
        if button:
            self.material_list.selection_remove(self.material_list.selection())

    def add_register(self):
        if self.check_fields():
            query = "INSERT INTO MATERIAL VALUES(?, ?, ?, ?, ?, ?)"
            param = (self.counter_ids(), self.txt_type.get().upper(), self.txt_mark.get().upper(),
                self.txt_model.get().upper(), self.path_img, self.txt_comments.get(1.0, tk.END))
            run_sql(self.name_database, query, param)
            messagebox.showinfo("Afegir registre", "Has afegit un registre correctament.")
            self.delete_fields()
            self.counter_ids()
            self.delete_material_list()
            self.filling_material_list()
            self.add_values()

    def update_register(self):  # falta seleccionar un registre
        if self.check_fields():
            query = "UPDATE MATERIAL SET TIPUS=?, MARCA=?, MODEL=?, FOTO=?, COMENTARIS=? WHERE ID=?"
            param = (self.txt_type.get().upper(), self.txt_mark.get().upper(),
                self.txt_model.get().upper(), self.path_img, self.txt_comments.get(1.0, tk.END), 
                self.material_list.item(self.material_list.selection()[0], "text"))
            run_sql(self.name_database, query, param)
            print(self.txt_comments.get(1.0, tk.END))
            messagebox.showinfo("Afegir registre", "Has actualitzat un registre correctament.")
            self.delete_fields()
            self.counter_ids()
            self.delete_material_list()
            self.filling_material_list()
            self.add_values()

    def delete_register(self):
        option = messagebox.askokcancel("Eliminar registre", "Estas segur d'eliminar el registre?")
        if option:
            query = "DELETE FROM MATERIAL WHERE ID=?"
            param = (self.material_list.item(self.material_list.selection()[0], "text"), )
            run_sql(self.name_database, query, param)
            messagebox.showinfo("Eliminar registre", "Has eliminat un registre correctament.")
            self.delete_fields()
            self.counter_ids()
            self.delete_material_list()
            self.filling_material_list()
            self.add_values()