import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, Toplevel



root = tk.Tk()
root.title("Inventory Management System")
root.geometry("800x600")
root.config(bg="lightgrey")

import sqlite3

conn = sqlite3.connect('inventory.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS products (
             id INTEGER PRIMARY KEY,
             name TEXT NOT NULL,
             price REAL NOT NULL,
             quantity INTEGER NOT NULL)''')
conn.commit()

def add_product():
    name = name_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()
    if name and price and quantity:
        c.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
        conn.commit()
        messagebox.showinfo("Success", "Product added successfully")
        clear_entries()
        display_products()
    else:
        messagebox.showerror("Error", "Please fill in all fields")

def display_products():
    products_tree.delete(*products_tree.get_children())
    for row in c.execute("SELECT * FROM products"):
        products_tree.insert('', 'end', values=row)

def clear_entries():
    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

name_label = tk.Label(root, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

price_label = tk.Label(root, text="Price:")
price_label.grid(row=1, column=0, padx=5, pady=5)
price_entry = tk.Entry(root)
price_entry.grid(row=1, column=1, padx=5, pady=5)

quantity_label = tk.Label(root, text="Quantity:")
quantity_label.grid(row=2, column=0, padx=5, pady=5)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Product", command=add_product)
add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

products_tree = ttk.Treeview(root, columns=("ID", "Name", "Price", "Quantity"), show="headings")
products_tree.heading("ID", text="ID")
products_tree.heading("Name", text="Name")
products_tree.heading("Price", text="Price")
products_tree.heading("Quantity", text="Quantity")
products_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

display_products()

def check_stock():
    low_stock_items = []
    for row in c.execute("SELECT * FROM products WHERE quantity < ?", (10,)):
        low_stock_items.append(row[1])
    if low_stock_items:
        messagebox.showwarning("Low Stock", f"The following items are running low in stock: {', '.join(low_stock_items)}")

# def record_sale():
#     if not products_tree.selection():
#         messagebox.showerror("Error", "Please select a product to sell")
#         return

#     selected_item = products_tree.selection()[0]
#     product_id = products_tree.item(selected_item, 'values')[0]
#     quantity_sold = simpledialog.askinteger("Sell Product", "Enter quantity sold:")
#     if quantity_sold:
#         c.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
#         current_quantity = c.fetchone()[0]
#         if current_quantity >= quantity_sold:
#             new_quantity = current_quantity - quantity_sold
#             c.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
#             conn.commit()
#             messagebox.showinfo("Success", "Sale recorded successfully")
#             display_products()
#         else:
#             messagebox.showerror("Error", "Insufficient stock")
#     else:
#         messagebox.showerror("Error", "Invalid quantity")


def record_sale():
    if not products_tree.selection():
        messagebox.showerror("Error", "Please select a product to sell")
        return

    selected_item = products_tree.selection()[0]
    product_id = products_tree.item(selected_item, 'values')[0]
    quantity_sold = simpledialog.askinteger("Sell Product", "Enter quantity sold:")
    if quantity_sold:
        c.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
        current_quantity = c.fetchone()[0]
        if current_quantity >= quantity_sold:
            new_quantity = current_quantity - quantity_sold
            c.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
            conn.commit()
            messagebox.showinfo("Success", "Sale recorded successfully")
            display_products()
        else:
            messagebox.showerror("Error", "Insufficient stock")
    else:
        messagebox.showerror("Error", "Invalid quantity")




# def record_sale():
#     selected_item = products_tree.selection()[0]
#     product_id = products_tree.item(selected_item, 'values')[0]
#     quantity_sold = simpledialog.askinteger("Sell Product", "Enter quantity sold:")
#     if quantity_sold:
#         c.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
#         current_quantity = c.fetchone()[0]
#         if current_quantity >= quantity_sold:
#             new_quantity = current_quantity - quantity_sold
#             c.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
#             conn.commit()
#             messagebox.showinfo("Success", "Sale recorded successfully")
#             display_products()
#         else:
#             messagebox.showerror("Error", "Insufficient stock")
#     else:
#         messagebox.showerror("Error", "Invalid quantity")

def generate_report():
    top_selling_items = []
    low_stock_items = []
    for row in c.execute("SELECT * FROM products ORDER BY quantity DESC LIMIT 5"):
        top_selling_items.append(row[1])
    for row in c.execute("SELECT * FROM products WHERE quantity < ?", (10,)):
        low_stock_items.append(row[1])
    report_text = f"Top Selling Items: {', '.join(top_selling_items)}\n\nLow Stock Items: {', '.join(low_stock_items)}"
    report_window = tk.Toplevel(root)
    report_window.title("Inventory Report")
    report_label = tk.Label(report_window, text=report_text)
    report_label.pack()

check_stock_button = tk.Button(root, text="Check Stock", command=check_stock)
check_stock_button.grid(row=5, column=0, padx=5, pady=5)

record_sale_button = tk.Button(root, text="Record Sale", command=record_sale)
record_sale_button.grid(row=5, column=1, padx=5, pady=5)

generate_report_button = tk.Button(root, text="Generate Report", command=generate_report)
generate_report_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()

