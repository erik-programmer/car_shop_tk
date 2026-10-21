import sqlite3
import tkinter as tk


class CarsSearchForm:
    def __init__(self, root) -> None:
        self.frame = tk.Frame(root)
        self.search_box = tk.Entry(self.frame)
        self.search_button = tk.Button(self.frame, text="Search")
        self.cars_list = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=5)
        self.edit_button = tk.Button(self.frame, text="Edit")
        self.add_button = tk.Button(self.frame, text="Add")
        self.delete_button = tk.Button(self.frame, text="Delete")

        self.frame.pack()
        self.search_box.pack()
        self.search_button.pack()
        self.cars_list.pack()
        self.edit_button.pack()
        self.add_button.pack()
        self.delete_button.pack()


root = tk.Tk()


conn = sqlite3.connect("cars.db")
results = conn.execute("SELECT car_id, model_name  FROM cars").fetchall()
CarsSearchForm(root)
conn.close()


root.mainloop()
