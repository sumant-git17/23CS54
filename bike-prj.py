import sqlite3
from sqlite3 import Error
import tkinter as tk
from tkinter import ttk, messagebox
import os

DB_FILE = "bikes.db"

# Delete DB if exists (fresh setup)
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bikes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                brand TEXT NOT NULL,
                built_year INTEGER,
                year INTEGER,
                price REAL
            )
        ''')
        conn.commit()
    except Error as e:
        print(f"Error creating table: {e}")

def add_bike(conn, model, brand, built_year, year, price):
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bikes (model, brand, built_year, year, price) VALUES (?, ?, ?, ?, ?)',
                       (model, brand, built_year, year, price))
        conn.commit()
        messagebox.showinfo("Success", "Bike added successfully.")
    except Error as e:
        messagebox.showerror("Error", str(e))

def get_all_bikes(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bikes")
    return cursor.fetchall()

# Bike data with price and built year
BIKE_MODEL_TO_BRAND = {
    "Classic 350":        {"brand": "Royal Enfield", "price": 190000, "built_year": 2009},
    "Interceptor 650":    {"brand": "Royal Enfield", "price": 280000, "built_year": 2018},
    "R15":                {"brand": "Yamaha",         "price": 180000, "built_year": 2008},
    "FZ":                 {"brand": "Yamaha",         "price": 120000, "built_year": 2008},
    "Apache RTR 310":     {"brand": "TVS",            "price": 240000, "built_year": 2017},
    "Pulsar NS400Z":      {"brand": "Bajaj",          "price": 192328, "built_year": 2022},
    "Splendor Plus":      {"brand": "Hero",           "price": 78926,  "built_year": 1994},
    "Duke 390":           {"brand": "KTM",            "price": 295000, "built_year": 2013},
    "CB Shine":           {"brand": "Honda",          "price": 95000,  "built_year": 2006},
    "Activa 6G":          {"brand": "Honda",          "price": 85000,  "built_year": 2020},
    "Ninja 300":          {"brand": "Kawasaki",       "price": 343000, "built_year": 2013},
    "CBR 250R":           {"brand": "Honda",          "price": 270000, "built_year": 2011},
    "Thunder 350":        {"brand": "Jawa",           "price": 180000, "built_year": 2021},
    "Ntorq 125":          {"brand": "TVS",            "price": 100000, "built_year": 2018},
    "Dio 125":            {"brand": "Honda",          "price": 74930,  "built_year": 2002},
    "Himalayan":          {"brand": "Royal Enfield",  "price": 450000, "built_year": 2016},
    "Fazer 25":           {"brand": "Yamaha",         "price": 130000, "built_year": 2020},
    "MT-15":              {"brand": "Yamaha",         "price": 180000, "built_year": 2018},
    "Avenger 220":        {"brand": "Bajaj",          "price": 125000, "built_year": 2005},
}

def main():
    conn = create_connection(DB_FILE)
    create_table(conn)

    root = tk.Tk()
    root.title("🚀 Bike Information System")
    root.geometry("800x550")
    root.configure(bg="#e1f5fe")  # Light blue background

    style = ttk.Style()
    style.theme_use("clam")  # Use a modern theme
    style.configure("TLabel", background="#e1f5fe", foreground="#0d47a1", font=('Arial', 10, 'bold'))
    style.configure("TButton", font=('Arial', 10, 'bold'), padding=6)
    style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), foreground="#ffffff", background="#0288d1")
    style.configure("Treeview", font=('Arial', 10), rowheight=25)

    bike_models = list(BIKE_MODEL_TO_BRAND.keys())

    tk.Label(root, text="Model").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    model_combobox = ttk.Combobox(root, values=bike_models, state="readonly", width=30)
    model_combobox.grid(row=0, column=1, padx=10, pady=5)
    model_combobox.set(bike_models[0])

    tk.Label(root, text="Brand").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    brand_var = tk.StringVar()
    brand_entry = tk.Entry(root, textvariable=brand_var, state="readonly", width=33)
    brand_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Built Year").grid(row=2, column=0, padx=10, pady=5, sticky='w')
    built_year_var = tk.StringVar()
    built_year_entry = tk.Entry(root, textvariable=built_year_var, state="readonly", width=33)
    built_year_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Your Year").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    year_entry = tk.Entry(root, width=35)
    year_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(root, text="Price (₹)").grid(row=4, column=0, padx=10, pady=5, sticky='w')
    price_var = tk.StringVar()
    price_entry = tk.Entry(root, textvariable=price_var, width=35)
    price_entry.grid(row=4, column=1, padx=10, pady=5)

    def on_model_change(event):
        selected_model = model_combobox.get()
        data = BIKE_MODEL_TO_BRAND.get(selected_model, {})
        brand_var.set(data.get("brand", ""))
        price_var.set(str(data.get("price", "")))
        built_year_var.set(str(data.get("built_year", "")))

    model_combobox.bind("<<ComboboxSelected>>", on_model_change)

    first_model = bike_models[0]
    brand_var.set(BIKE_MODEL_TO_BRAND[first_model]["brand"])
    price_var.set(str(BIKE_MODEL_TO_BRAND[first_model]["price"]))
    built_year_var.set(str(BIKE_MODEL_TO_BRAND[first_model]["built_year"]))

    def handle_add_bike():
        model = model_combobox.get().strip()
        brand = brand_var.get().strip()
        built_year = built_year_var.get().strip()
        year = year_entry.get().strip()
        price = price_var.get().strip()

        if not model or not brand or not built_year or not year or not price:
            messagebox.showwarning("Input Error", "Please fill all fields")
            return
        if not built_year.isdigit() or not year.isdigit():
            messagebox.showwarning("Input Error", "Years must be numbers")
            return
        try:
            price_val = float(price)
        except ValueError:
            messagebox.showwarning("Input Error", "Price must be a number")
            return

        add_bike(conn, model, brand, int(built_year), int(year), price_val)
        refresh_bikes()
        year_entry.delete(0, tk.END)
        price_var.set(str(BIKE_MODEL_TO_BRAND[model]["price"]))

    ttk.Button(root, text="Add Bike", command=handle_add_bike).grid(row=5, column=0, columnspan=2, pady=10)

    columns = ("ID", "Model", "Brand", "Built Year", "Year", "Price (₹)")
    bike_list = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns:
        bike_list.heading(col, text=col)
        bike_list.column(col, width=120 if col != "Price (₹)" else 100, anchor="center")
    bike_list.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    def refresh_bikes():
        for row in bike_list.get_children():
            bike_list.delete(row)
        for bike in get_all_bikes(conn):
            bike_list.insert('', tk.END, values=bike)

    ttk.Button(root, text="Refresh List", command=refresh_bikes).grid(row=7, column=0, columnspan=2)

    root.grid_rowconfigure(6, weight=1)
    root.grid_columnconfigure(1, weight=1)

    refresh_bikes()
    root.mainloop()

if __name__ == "__main__":
    main()
