import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="piyush"
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS contact_management")
cursor.execute("USE contact_management")
cursor.execute("CREATE TABLE IF NOT EXISTS contacts (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL,phone VARCHAR(20) NOT NULL, email VARCHAR(255) NOT NULL)")


# Function to add a contact
def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    
    if name and phone and email:
        cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)", (name, phone, email))
        conn.commit()
        messagebox.showinfo("Success", "Contact added successfully!")
        clear_entries()
        load_contacts()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Function to update a contact
def update_contact():
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.item(selected_item)["values"][0]
        name = entry_name.get()
        phone = entry_phone.get()
        email = entry_email.get()

        cursor.execute("UPDATE contacts SET name = %s, phone = %s, email = %s WHERE id = %s", (name, phone, email, item_id))
        conn.commit()
        messagebox.showinfo("Success", "Contact updated successfully!")
        clear_entries()
        load_contacts()
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to update")

# Function to delete a contact
def delete_contact():
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.item(selected_item)["values"][0]
        cursor.execute("DELETE FROM contacts WHERE id = %s", (item_id,))
        conn.commit()
        messagebox.showinfo("Success", "Contact deleted successfully!")
        load_contacts()
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to delete")

# Function to load contacts into the tree view
def load_contacts():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM contacts")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# Function to clear entry fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# Function to populate entry fields when a contact is selected
def select_contact(event):
    selected_item = tree.selection()
    if selected_item:
        item_id, name, phone, email = tree.item(selected_item)["values"]
        entry_name.delete(0, tk.END)
        entry_name.insert(tk.END, name)
        entry_phone.delete(0, tk.END)
        entry_phone.insert(tk.END, phone)
        entry_email.delete(0, tk.END)
        entry_email.insert(tk.END, email)

# GUI setup
app = tk.Tk()
app.title("Contact Management System")
app.geometry("820x410")

# Input fields
tk.Label(app, text="Name").grid(row=0, column=0, padx=10, pady=10)
entry_name = tk.Entry(app)
entry_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(app, text="Phone").grid(row=1, column=0, padx=10, pady=10)
entry_phone = tk.Entry(app)
entry_phone.grid(row=1, column=1, padx=10, pady=10)

tk.Label(app, text="Email").grid(row=2, column=0, padx=10, pady=10)
entry_email = tk.Entry(app)
entry_email.grid(row=2, column=1, padx=10, pady=10)

# Buttons
tk.Button(app, text="Add Contact", command=add_contact).grid(row=3, column=0, padx=10, pady=10)
tk.Button(app, text="Update Contact", command=update_contact).grid(row=3, column=1, padx=10, pady=10)
tk.Button(app, text="Delete Contact", command=delete_contact).grid(row=3, column=2, padx=10, pady=10)

# Tree view for contacts
columns = ("ID", "Name", "Phone", "Email")
tree = ttk.Treeview(app, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
tree.bind("<<TreeviewSelect>>", select_contact)

# Load contacts initially
load_contacts()

app.mainloop()

# Close the MySQL connection on exit
conn.close()
