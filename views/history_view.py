import tkinter as tk
from tkinter import ttk
import sqlite3

def ver_historial_movimientos():
    ventana = tk.Tk()
    ventana.title("Historial de Movimientos")
    ventana.geometry("800x400")

    columnas = ("ID", "Producto", "Tipo", "Cantidad", "Fecha")

    tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(fill=tk.BOTH, expand=True)

    conn = sqlite3.connect("db/inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT movimientos.id, productos.nombre, movimientos.tipo, 
               movimientos.cantidad, movimientos.fecha 
        FROM movimientos 
        JOIN productos ON productos.id = movimientos.producto_id
        ORDER BY movimientos.fecha DESC
    """)
    movimientos = cursor.fetchall()
    conn.close()

    for mov in movimientos:
        tabla.insert("", tk.END, values=mov)

    ventana.mainloop()
