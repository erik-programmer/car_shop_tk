import tkinter as tk
import sqlite3
from typing import List


class Author:
    def __init__(self, result) -> None:
        self.id = result[0]
        self.name = result[1]
        self.birth_year = result[3]


class AuthorListForm:
    def __init__(self, root, authors: List[Author], delete_author_callback) -> None:
        self.frame = tk.Frame(root)
        self.delete_author_callback = delete_author_callback
        self.authors = authors
        self.delete_button = tk.Button(
            self.frame, text="Delete", command=self.delete_button_clicked
        )
        self.author_list_box = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=5)
        for author in authors:
            self.author_list_box.insert(tk.END, f"{author.name} ({author.birth_year})")
        self.frame.pack()
        self.author_list_box.pack()
        self.delete_button.pack()

    def delete_button_clicked(self):
        selected = self.author_list_box.curselection()
        if selected:
            a = self.authors[selected[0]]
            self.authors.remove(a)
            self.author_list_box.delete(selected[0], selected[0])
            self.delete_author_callback(a)


def delete_author_from_db(author: Author):
    conn.execute(f"delete from authors where author_id = {author.id}")
    conn.commit()


root = tk.Tk()
root.geometry("500x500")
conn = sqlite3.connect("authors.db")

results = conn.execute("SELECT * FROM authors ORDER BY name").fetchall()
authors: List[Author] = list(Author(result) for result in results)
authorlistform = AuthorListForm(root, authors, delete_author_from_db)
root.mainloop()

conn.close()
