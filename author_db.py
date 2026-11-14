import tkinter as tk
import sqlite3
from typing import List

# Plan


class Author:
    def __init__(self, result) -> None:
        self.id = result[0]
        self.name = result[1]
        self.birth_year = result[3]


class AuthorAddForm:
    def __init__(self, root, add_author_callback) -> None:
        self.frame = tk.Frame(root)

        self.name_label = tk.Label(self.frame, text="Name")
        self.name_textbox = tk.Entry(self.frame)
        self.country_label = tk.Label(self.frame, text="Country")
        self.country_textbox = tk.Entry(self.frame)
        self.year_label = tk.Label(self.frame, text="Year")
        self.year_textbox = tk.Entry(self.frame)

        self.add_author_callback = add_author_callback

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
        self.add_author_callback(
            self.name_textbox.get(), self.country_textbox.get(), self.year_textbox.get()
        )
        self.frame.destroy()


class AuthorListForm:
    def __init__(
        self,
        root,
        authors: List[Author],
        delete_author_callback,
        create_add_author_form_callback,
    ) -> None:
        self.frame = tk.Frame(root)
        self.delete_author_callback = delete_author_callback
        self.create_add_author_form_callback = create_add_author_form_callback
        self.authors = authors
        self.delete_button = tk.Button(
            self.frame, text="Delete", command=self.delete_button_clicked
        )
        self.add_button = tk.Button(
            self.frame, text="Add", command=self.add_button_clicked
        )
        self.author_list_box = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=5)
        for author in authors:
            self.author_list_box.insert(tk.END, f"{author.name} ({author.birth_year})")
        self.frame.pack()
        self.author_list_box.pack()
        self.delete_button.pack()
        self.add_button.pack()

    def add_button_clicked(self):
        self.frame.destroy()
        self.create_add_author_form_callback()

    def delete_button_clicked(self):
        selected = self.author_list_box.curselection()
        if selected:
            a = self.authors[selected[0]]
            self.frame.destroy()
            self.delete_author_callback(a)


class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.conn = sqlite3.connect("authors.db")

    def create_author_list_form(self):
        results = self.conn.execute("SELECT * FROM authors ORDER BY name").fetchall()
        authors: List[Author] = list(Author(result) for result in results)
        AuthorListForm(
            self.root, authors, self.delete_author_from_db, self.create_add_author_form
        )

    def delete_author_from_db(self, author: Author):
        self.conn.execute(f"delete from authors where author_id = {author.id}")
        self.conn.commit()
        self.create_author_list_form()

    def insert_author_to_db(self, name, country, birth_year):
        self.conn.execute(
            f"INSERT INTO authors (name,country,birth_year) Values ('{name}','{country}',{birth_year})"
        )
        self.conn.commit()
        self.create_author_list_form()

    def create_add_author_form(self):
        authoraddform = AuthorAddForm(self.root, self.insert_author_to_db)

    def run(self):
        self.root.mainloop()
        self.conn.close()


main = Main()
main.create_author_list_form()
main.run()
