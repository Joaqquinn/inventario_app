import tkinter as tk
from tkinter import ttk
from utils.style import aplicar_estilos_generales
import sqlite3

def listar_productos():
    # Crear ventana
    ventana = tk.Tk()
    ventana.title("Listado de Productos")
    ventana.geometry("800x400")

    # Crear tabla tipo Treeview
    columnas = ("ID", "Nombre", "Código", "Stock", "Ubicación", "Proveedor", "Precio")

    tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)

    tabla.pack(fill=tk.BOTH, expand=True)

    # Obtener datos desde la base de datos
    conn = sqlite3.connect("db/inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, codigo, stock, ubicacion, proveedor, precio FROM productos")
    productos = cursor.fetchall()
    conn.close()

    # Agregar datos a la tabla
    for producto in productos:
        tabla.insert("", tk.END, values=producto)

    ventana.mainloop()
