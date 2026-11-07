import tkinter as tk
import sqlite3
from typing import List


class Author:
    def __init__(self, result) -> None:
        self.id = result[0]
        self.name = result[1]
        self.birth_year = result[3]


class AuthorListForm:
    def __init__(self, root, authors: List[Author]) -> None:
        self.frame = tk.Frame(root)
        self.authors = authors
        self.author_list_box = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=5)
        for author in authors:
            self.author_list_box.insert(tk.END, f"{author.name} ({author.birth_year})")
        self.frame.pack()
        self.author_list_box.pack()


root = tk.Tk()
root.geometry("500x500")
conn = sqlite3.connect("authors.db")

results = conn.execute("SELECT * FROM authors ORDER BY name").fetchall()
authors: List[Author] = list(Author(result) for result in results)
authorlistform = AuthorListForm(root, authors)
root.mainloop()

conn.close()
