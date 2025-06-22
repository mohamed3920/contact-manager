# Project: Contact Manager (Advanced)
# Features: Add, Search, Edit, Delete, and List Contacts with SQLite + Tkinter

import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

# Functions
def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()

    if name and phone:
        conn = sqlite3.connect("contacts.db")
        c = conn.cursor()
        c.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        conn.commit()
        conn.close()
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        messagebox.showinfo("Success", "Contact added successfully!")
        view_contacts()
    else:
        messagebox.showerror("Error", "Name and phone are required.")

def view_contacts():
    listbox.delete(0, tk.END)
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    for row in c.fetchall():
        listbox.insert(tk.END, f"{row[0]} - {row[1]} | {row[2]} | {row[3]}")
    conn.close()

def delete_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No contact selected.")
        return
    contact_id = int(listbox.get(selected[0]).split(" - ")[0])
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    view_contacts()
    messagebox.showinfo("Deleted", "Contact deleted.")

def search_contact():
    query = entry_search.get()
    listbox.delete(0, tk.END)
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?", (f"%{query}%", f"%{query}%"))
    for row in c.fetchall():
        listbox.insert(tk.END, f"{row[0]} - {row[1]} | {row[2]} | {row[3]}")
    conn.close()

def edit_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No contact selected.")
        return

    contact_id = int(listbox.get(selected[0]).split(" - ")[0])
    new_name = entry_name.get()
    new_phone = entry_phone.get()
    new_email = entry_email.get()

    if new_name and new_phone:
        conn = sqlite3.connect("contacts.db")
        c = conn.cursor()
        c.execute("UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?", (new_name, new_phone, new_email, contact_id))
        conn.commit()
        conn.close()
        view_contacts()
        messagebox.showinfo("Updated", "Contact updated successfully.")
    else:
        messagebox.showerror("Error", "Name and phone are required.")

# GUI setup
init_db()

window = tk.Tk()
window.title("Contact Manager")

# Top fields
tk.Label(window, text="Name:").grid(row=0, column=0)
entry_name = tk.Entry(window)
entry_name.grid(row=0, column=1)

tk.Label(window, text="Phone:").grid(row=1, column=0)
entry_phone = tk.Entry(window)
entry_phone.grid(row=1, column=1)

tk.Label(window, text="Email:").grid(row=2, column=0)
entry_email = tk.Entry(window)
entry_email.grid(row=2, column=1)

# Buttons
tk.Button(window, text="Add Contact", command=add_contact).grid(row=0, column=2)
tk.Button(window, text="Edit Selected", command=edit_contact).grid(row=1, column=2)
tk.Button(window, text="Delete Selected", command=delete_contact).grid(row=2, column=2)

# Search bar
tk.Label(window, text="Search:").grid(row=3, column=0)
entry_search = tk.Entry(window)
entry_search.grid(row=3, column=1)
tk.Button(window, text="Search", command=search_contact).grid(row=3, column=2)

# Listbox for contacts
listbox = tk.Listbox(window, width=60)
listbox.grid(row=4, column=0, columnspan=3)
tk.Button(window, text="Refresh", command=view_contacts).grid(row=5, column=1)

view_contacts()
window.mainloop()
