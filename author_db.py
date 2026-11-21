import tkinter as tk
import sqlite3
from typing import List

# Plan
# How to update one author
# 1. Add update button to list form (with callback to open AuthorDetailsForm)
# 2. Add function to AuthorDetailsForm to set values like name, country etc. of selected author (load them from db)


class Author:
    def __init__(self, result) -> None:
        self.id = result[0]
        self.name = result[1]
        self.birth_year = result[3]


class AuthorDetailsForm:
    def __init__(self, root, write_db_callback, is_update) -> None:
        self.frame = tk.Frame(root)

        self.name_label = tk.Label(self.frame, text="Name")
        self.name_textbox = tk.Entry(self.frame)
        self.country_label = tk.Label(self.frame, text="Country")
        self.country_textbox = tk.Entry(self.frame)
        self.year_label = tk.Label(self.frame, text="Year")
        self.year_textbox = tk.Entry(self.frame)
        self.is_update = is_update
        self.write_db_callback = write_db_callback

        self.ok_button = tk.Button(
            self.frame, text="Okay", command=self.ok_button_clicked
        )
        self.frame.pack()
        self.ok_button.pack()

        self.name_label.pack()
        self.name_textbox.pack()
        self.country_label.pack()
        self.country_textbox.pack()
        self.year_label.pack()
        self.year_textbox.pack()

    def ok_button_clicked(self):
        if self.is_update:
            self.write_db_callback(
                self.id,
                self.name_textbox.get(),
                self.country_textbox.get(),
                self.year_textbox.get(),
            )
        else:
            self.write_db_callback(
                self.name_textbox.get(),
                self.country_textbox.get(),
                self.year_textbox.get(),
            )

        self.frame.destroy()

    def set_values(self, id, name, country, birthyear):
        self.id = id
        self.name_textbox.insert(0, name)
        self.country_textbox.insert(0, country)
        self.year_textbox.insert(0, birthyear)


class AuthorListForm:
    def __init__(
        self,
        root,
        authors: List[Author],
        delete_author_callback,
        create_add_author_form_callback,
        create_update_author_form_callback,
    ) -> None:
        self.frame = tk.Frame(root)
        self.delete_author_callback = delete_author_callback
        self.create_update_author_form_callback = create_update_author_form_callback
        self.create_add_author_form_callback = create_add_author_form_callback
        self.authors = authors
        self.delete_button = tk.Button(
            self.frame, text="Delete", command=self.delete_button_clicked
        )
        self.add_button = tk.Button(
            self.frame, text="Add", command=self.add_button_clicked
        )
        self.update_button = tk.Button(
            self.frame, text="Update", command=self.update_button_clicked
        )
        self.author_list_box = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=5)
        for author in authors:
            self.author_list_box.insert(tk.END, f"{author.name} ({author.birth_year})")
        self.frame.pack()
        self.author_list_box.pack()
        self.delete_button.pack()
        self.add_button.pack()
        self.update_button.pack()

    def add_button_clicked(self):
        self.frame.destroy()
        self.create_add_author_form_callback()

    def delete_button_clicked(self):
        selected = self.author_list_box.curselection()
        if selected:
            a = self.authors[selected[0]]
            self.frame.destroy()
            self.delete_author_callback(a)

    def update_button_clicked(self):
        selected = self.author_list_box.curselection()
        if selected:
            a = self.authors[selected[0]]
            self.frame.destroy()
            self.create_update_author_form_callback(a)


class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.conn = sqlite3.connect("authors.db")

    def create_author_list_form(self):
        results = self.conn.execute("SELECT * FROM authors ORDER BY name").fetchall()
        authors: List[Author] = list(Author(result) for result in results)
        AuthorListForm(
            self.root,
            authors,
            self.delete_author_from_db,
            self.create_add_author_form,
            self.create_update_author_form,
        )

    def delete_author_from_db(self, author: Author):
        self.conn.execute(f"delete from authors where author_id = {author.id}")
        self.conn.commit()
        self.create_author_list_form()

    def create_update_author_form(self, author: Author):
        r = self.conn.execute(
            f"SELECT * FROM authors Where author_id = {author.id}"
        ).fetchone()
        authorupdateform = AuthorDetailsForm(self.root, self.update_author_in_db, True)
        authorupdateform.set_values(r[0], r[1], r[2], r[3])

    def update_author_in_db(self, id, name, country, birth_year):
        self.conn.execute(
            f"UPDATE authors SET name = '{name}', country='{country}', birth_year={birth_year} WHERE author_id={id}"
        )
        self.conn.commit()
        self.create_author_list_form()

    def insert_author_to_db(self, name, country, birth_year):
        self.conn.execute(
            f"INSERT INTO authors (name,country,birth_year) Values ('{name}','{country}',{birth_year})"
        )
        self.conn.commit()
        self.create_author_list_form()

    def create_add_author_form(self):
        authoraddform = AuthorDetailsForm(self.root, self.insert_author_to_db, False)

    def run(self):
        self.root.mainloop()
        self.conn.close()


main = Main()
main.create_author_list_form()
main.run()
