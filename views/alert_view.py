import tkinter as tk
from tkinter import ttk
import sqlite3

def mostrar_alertas_stock_bajo():
    ventana = tk.Tk()
    ventana.title("Productos con stock bajo")
    ventana.geometry("700x300")

    columnas = ("ID", "Nombre", "Stock", "Stock Mínimo")

    tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(fill=tk.BOTH, expand=True)

    conn = sqlite3.connect("db/inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre, stock, stock_minimo 
        FROM productos 
        WHERE stock <= stock_minimo
    """)
    productos_bajo_stock = cursor.fetchall()
    conn.close()

    for p in productos_bajo_stock:
        tabla.insert("", tk.END, values=p)

    if not productos_bajo_stock:
        tk.Label(ventana, text="No hay productos con stock bajo 👌").pack(pady=10)

    ventana.mainloop()
