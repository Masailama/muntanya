import sqlite3
from PIL import Image, ImageTk
from tkinter import filedialog


def run_sql(name, query, parameters=(), read=False):
    connection = sqlite3.connect(name)
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    data = cursor.fetchall()
    connection.commit()
    connection.close()
    if read:
        return data

def transform_image(path_image, w_image, h_image):
    image = Image.open(path_image)
    image = image.resize((w_image, h_image), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    return image

def add_image():
    name = filedialog.askopenfilename(title="Buscar imatge", 
        filetypes=(("Imatges", "*.jpg *.jpeg *.png"),))
    return name