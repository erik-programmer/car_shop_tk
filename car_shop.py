import sqlite3
import tkinter as tk


class Category:
    def __init__(self, category_id, name, description) -> None:
        self.category_id = category_id
        self.name = name
        self.description = description


class CarDetailsForm:
    def __init__(self, root, categories: list[Category], add_car_callback) -> None:
        self.add_car_callback = add_car_callback
        self.frame = tk.Frame(root)
        self.categories = categories
        self.model_name_label = tk.Label(self.frame, text="Model name")
        self.model_name_box = tk.Entry(self.frame)
        self.year_label = tk.Label(self.frame, text="Year")
        self.year_box = tk.Entry(self.frame)
        self.category_label = tk.Label(self.frame, text="Category")
        self.category_list = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=5)
        for r in self.categories:
            self.category_list.insert(tk.END, f"{r.name} ({r.description})")
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

    def set_data(self, mn, y, c_id):
        self.model_name_box.insert(0, mn)
        self.year_box.insert(0, y)
        for i, c in enumerate(self.categories):
            if c_id == c.category_id:
                self.category_list.select_set(i, i)

    def ok_button_clicked(self):
        model_name_text = self.model_name_box.get()
        year_text = self.year_box.get()
        selected = self.category_list.curselection()[0]
        self.frame.destroy()
        self.add_car_callback(
            model_name_text, year_text, self.categories[selected].category_id
        )


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
        cars: list[Car],
        search_button_callback,
        delete_button_callback,
        add_button_callback,
        edit_button_callback,
    ) -> None:
        self.add_button_callback = add_button_callback
        self.search_button_callback = search_button_callback
        self.frame = tk.Frame(root)
        self.search_box = tk.Entry(self.frame)
        self.search_button = tk.Button(
            self.frame, text="Search", command=self.search_button_clicked
        )
        self.edit_button_callback = edit_button_callback
        self.cars_list = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=5)
        self.show_cars(cars)
        self.edit_button = tk.Button(
            self.frame, text="Edit", command=self.edit_button_clicked
        )
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
            c = self.cars[selected[0]]
            self.cars.remove(c)
            self.delete_button_callback(c.car_id)

    def search_button_clicked(self):
        self.search_button_callback(self.search_box.get())

    def show_cars(self, cars: list[Car]):
        self.cars = cars
        self.cars_list.delete(0, self.cars_list.size())
        for r in cars:
            self.cars_list.insert(
                tk.END, f"{r.model_name} ({r.year}, {r.category_name})"
            )

    def edit_button_clicked(self):
        selected = self.cars_list.curselection()
        if selected:
            self.frame.destroy()
            self.edit_button_callback(self.cars[selected[0]].car_id)

    def add_button_clicked(self):
        self.frame.destroy()
        self.add_button_callback()


root = tk.Tk()
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

    cardetailsform = CarDetailsForm(
        root, list(Category(r[0], r[1], r[2]) for r in results), execute_add_car
    )


def execute_edit_car(car_id):

    result = conn.execute(
        f"SELECT model_name, year, category_id FROM cars WHERE car_id= {car_id}"
    ).fetchone()
    categories = conn.execute(
        "SELECT category_id ,category_name, description FROM car_categories"
    ).fetchall()
    car_details_form = CarDetailsForm(
        root, list(Category(r[0], r[1], r[2]) for r in categories), execute_add_car
    )
    car_details_form.set_data(result[0], result[1], result[2])


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
        execute_edit_car,
    )
    return car_search_form


car_search_form = create_car_search_form()


root.mainloop()
conn.close()
