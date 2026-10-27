import sqlite3
import tkinter as tk


class CarDetailsForm:
    def __init__(self, root, results, add_car_callback) -> None:
        self.add_car_callback = add_car_callback
        self.frame = tk.Frame(root)
        self.results = results
        self.model_name_label = tk.Label(self.frame, text="Model name")
        self.model_name_box = tk.Entry(self.frame)
        self.year_label = tk.Label(self.frame, text="Year")
        self.year_box = tk.Entry(self.frame)
        self.category_label = tk.Label(self.frame, text="Category")
        self.category_list = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=5)
        for r in self.results:
            self.category_list.insert(tk.END, f"{r[1]} ({r[2]})")
        self.ok_button = tk.Button(
            self.frame, text="Ok", command=self.ok_button_clicked
        )
        self.frame.pack()
        self.model_name_label.pack()
        self.model_name_box.pack()
        self.year_label.pack()
        self.year_box.pack()
        self.category_label.pack()
        self.category_list.pack()
        self.ok_button.pack()

    def ok_button_clicked(self):
        model_name_text = self.model_name_box.get()
        year_text = self.year_box.get()
        selected = self.category_list.curselection()[0]
        self.frame.destroy()
        self.add_car_callback(model_name_text, year_text, self.results[selected][0])


# ok not okay


class Car:
    def __init__(self, model_name, year, category_name, car_id) -> None:
        self.model_name = model_name
        self.year = year
        self.category_name = category_name
        self.car_id = car_id


class CarsSearchForm:
    def __init__(
        self,
        root,
        results: list[Car],
        search_button_callback,
        delete_button_callback,
        add_button_callback,
    ) -> None:
        self.add_button_callback = add_button_callback
        self.search_button_callback = search_button_callback
        self.frame = tk.Frame(root)
        self.search_box = tk.Entry(self.frame)
        self.search_button = tk.Button(
            self.frame, text="Search", command=self.search_button_clicked
        )
        self.cars_list = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=5)
        self.show_cars(results)
        self.edit_button = tk.Button(self.frame, text="Edit")
        self.add_button = tk.Button(
            self.frame, text="Add", command=self.add_button_clicked
        )
        self.delete_button = tk.Button(
            self.frame, text="Delete", command=self.delete_button_clicked
        )
        self.delete_button_callback = delete_button_callback

        self.frame.pack()
        self.search_box.pack()
        self.search_button.pack()
        self.cars_list.pack()
        self.edit_button.pack()
        self.add_button.pack()
        self.delete_button.pack()

    def delete_button_clicked(self):
        selected = self.cars_list.curselection()
        if selected:
            self.cars_list.delete(selected[0])
            c = self.results[selected[0]]
            self.results.remove(c)
            self.delete_button_callback(c.car_id)

    def search_button_clicked(self):
        self.search_button_callback(self.search_box.get())

    def show_cars(self, results: list[Car]):
        self.results = results
        self.cars_list.delete(0, self.cars_list.size())
        for r in results:
            self.cars_list.insert(
                tk.END, f"{r.model_name} ({r.year}, {r.category_name})"
            )

    def add_button_clicked(self):
        self.frame.destroy()
        self.add_button_callback()


root = tk.Tk()
# modelname (year, category_name)
conn = sqlite3.connect("cars.db")


def execute_add_car(mn, y, c_id):
    global car_search_form
    conn.execute(
        f"INSERT INTO cars (model_name,year,category_id) VALUES ('{mn}',{y},{c_id})"
    )
    conn.commit()
    car_search_form = create_car_search_form()


def execute_add():
    results = conn.execute(
        "SELECT category_id ,category_name, description FROM car_categories"
    ).fetchall()
    print(results)

    cardetailsform = CarDetailsForm(root, results, execute_add_car)


def execute_delete(car_id):
    conn.execute(f"DELETE FROM cars WHERE car_id = {car_id}")
    conn.commit()


def execute_search(text):
    results = conn.execute(
        f"SELECT  model_name,year , car_categories.category_name, car_id FROM cars JOIN car_categories ON cars.category_id=car_categories.category_id WHERE cars.model_name LIKE '%{text}%' OR car_categories.category_name LIKE '%{text}%' ORDER BY model_name"
    ).fetchall()
    car_search_form.show_cars(list(Car(t[0], t[1], t[2], t[3]) for t in results))


def create_car_search_form():
    results = conn.execute(
        "SELECT  model_name,year , car_categories.category_name, car_id FROM cars JOIN car_categories ON cars.category_id=car_categories.category_id ORDER BY model_name"
    ).fetchall()
    print(results)
    car_search_form = CarsSearchForm(
        root,
        list(Car(t[0], t[1], t[2], t[3]) for t in results),
        execute_search,
        execute_delete,
        execute_add,
    )
    return car_search_form


car_search_form = create_car_search_form()


root.mainloop()
conn.close()
