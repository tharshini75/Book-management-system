import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Database Connection
conn = sqlite3.connect("library.db")
cursor = conn.cursor()


# Create Books Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name TEXT,
    author TEXT,
    category TEXT,
    quantity INTEGER
)
""")

conn.commit()


# Main Window
root = tk.Tk()
root.title("Library Management System")
root.geometry("750x550")
root.configure(bg="#f2f6ff")


# Title
title = tk.Label(
    root,
    text="Library Management System",
    font=("Arial",22,"bold"),
    bg="#1e3a8a",
    fg="white",
    pady=10
)

title.pack(fill="x")


# Input Frame
frame = tk.Frame(
    root,
    bg="#f2f6ff"
)

frame.pack(pady=20)


# Book Name
tk.Label(
    frame,
    text="Book Name",
    bg="#f2f6ff",
    font=("Arial",11,"bold")
).grid(row=0,column=0,padx=10,pady=5)

book_entry = tk.Entry(
    frame,
    width=30
)

book_entry.grid(row=0,column=1)


# Author
tk.Label(
    frame,
    text="Author",
    bg="#f2f6ff",
    font=("Arial",11,"bold")
).grid(row=1,column=0,padx=10,pady=5)

author_entry = tk.Entry(
    frame,
    width=30
)

author_entry.grid(row=1,column=1)


# Category
tk.Label(
    frame,
    text="Category",
    bg="#f2f6ff",
    font=("Arial",11,"bold")
).grid(row=2,column=0,padx=10,pady=5)

category_entry = tk.Entry(
    frame,
    width=30
)

category_entry.grid(row=2,column=1)


# Quantity
tk.Label(
    frame,
    text="Quantity",
    bg="#f2f6ff",
    font=("Arial",11,"bold")
).grid(row=3,column=0,padx=10,pady=5)

quantity_entry = tk.Entry(
    frame,
    width=30
)

quantity_entry.grid(row=3,column=1)



# Add Book Function

def add_book():

    book = book_entry.get()
    author = author_entry.get()
    category = category_entry.get()
    quantity = quantity_entry.get()


    if book=="" or author=="" or quantity=="":
        messagebox.showerror(
            "Error",
            "Fill required fields"
        )
        return


    cursor.execute(
        """
        INSERT INTO books(
        book_name,
        author,
        category,
        quantity
        )
        VALUES(?,?,?,?)
        """,
        (
            book,
            author,
            category,
            quantity
        )
    )

    conn.commit()


    messagebox.showinfo(
        "Success",
        "Book Added Successfully"
    )


    clear_fields()
    view_books()



# Clear Function

def clear_fields():

    book_entry.delete(0,tk.END)
    author_entry.delete(0,tk.END)
    category_entry.delete(0,tk.END)
    quantity_entry.delete(0,tk.END)



# Table

columns = (
    "ID",
    "Book Name",
    "Author",
    "Category",
    "Quantity"
)


book_table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=8
)


for col in columns:
    book_table.heading(
        col,
        text=col
    )

    book_table.column(
        col,
        width=120
    )


book_table.pack(pady=20)



# View Books

def view_books():

    for row in book_table.get_children():
        book_table.delete(row)


    cursor.execute(
        "SELECT * FROM books"
    )

    books = cursor.fetchall()


    for book in books:
        book_table.insert(
            "",
            tk.END,
            values=book
        )



# Buttons

button_frame = tk.Frame(root,bg="#f2f6ff")
button_frame.pack()


add_btn = tk.Button(
    button_frame,
    text="Add Book",
    width=15,
    bg="#2563eb",
    fg="white",
    command=add_book
)

add_btn.grid(row=0,column=0,padx=10)


view_btn = tk.Button(
    button_frame,
    text="View Books",
    width=15,
    bg="#16a34a",
    fg="white",
    command=view_books
)

view_btn.grid(row=0,column=1,padx=10)



# Display Existing Data
# ==========================
# Search Book
# ==========================

search_frame = tk.Frame(root, bg="#f2f6ff")
search_frame.pack()


tk.Label(
    search_frame,
    text="Search Book",
    bg="#f2f6ff",
    font=("Arial",11,"bold")
).grid(row=0,column=0,padx=5)


search_entry = tk.Entry(search_frame)
search_entry.grid(row=0,column=1,padx=5)


def search_book():

    name = search_entry.get()

    for row in book_table.get_children():
        book_table.delete(row)


    cursor.execute(
        "SELECT * FROM books WHERE book_name LIKE ?",
        ('%'+name+'%',)
    )

    result = cursor.fetchall()


    for book in result:
        book_table.insert(
            "",
            tk.END,
            values=book
        )


search_btn = tk.Button(
    search_frame,
    text="Search",
    command=search_book,
    bg="#7c3aed",
    fg="white"
)

search_btn.grid(row=0,column=2,padx=5)

# ==========================
# Select Book
# ==========================

def select_book(event):

    selected = book_table.focus()

    if selected:

        values = book_table.item(selected)["values"]


        book_entry.delete(0,tk.END)
        book_entry.insert(0,values[1])


        author_entry.delete(0,tk.END)
        author_entry.insert(0,values[2])


        category_entry.delete(0,tk.END)
        category_entry.insert(0,values[3])


        quantity_entry.delete(0,tk.END)
        quantity_entry.insert(0,values[4])



book_table.bind(
    "<ButtonRelease-1>",
    select_book
)


# ==========================
# Update Book
# ==========================

def update_book():

    selected = book_table.focus()

    if selected == "":
        messagebox.showerror(
            "Error",
            "Select a book first"
        )
        return


    values = book_table.item(selected)["values"]

    book_id = values[0]


    cursor.execute(
        """
        UPDATE books
        SET book_name=?,
            author=?,
            category=?,
            quantity=?
        WHERE id=?
        """,
        (
            book_entry.get(),
            author_entry.get(),
            category_entry.get(),
            quantity_entry.get(),
            book_id
        )
    )

    conn.commit()


    messagebox.showinfo(
        "Updated",
        "Book Updated Successfully"
    )


view_books()

# ==========================
# Delete Book
# ==========================

def delete_book():

    selected = book_table.focus()

    if selected == "":
        messagebox.showerror(
            "Error",
            "Select a book first"
        )
        return


    values = book_table.item(selected)["values"]

    book_id = values[0]


    cursor.execute(
        "DELETE FROM books WHERE id=?",
        (book_id,)
    )

    conn.commit()


    messagebox.showinfo(
        "Deleted",
        "Book Deleted Successfully"
    )


    view_books()

update_btn = tk.Button(
    button_frame,
    text="Update Book",
    width=15,
    bg="#f59e0b",
    fg="white",
    command=update_book
)

update_btn.grid(row=0,column=2,padx=10)



delete_btn = tk.Button(
    button_frame,
    text="Delete Book",
    width=15,
    bg="#dc2626",
    fg="white",
    command=delete_book
)

delete_btn.grid(row=0,column=3,padx=10)

root.mainloop()