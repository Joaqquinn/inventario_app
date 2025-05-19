import tkinter as tk
from tkinter import ttk
from utils.style import aplicar_estilos_generales
import sqlite3

def listar_productos():
    def centrar_ventana(ventana, ancho, alto):
        ventana.update_idletasks()
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    ventana = tk.Tk()
    ventana.title("Listado de Productos")
    centrar_ventana(ventana, 850, 450)
    ventana.configure(bg="#f2f2f2")

    aplicar_estilos_generales()

    frame = tk.Frame(ventana, padx=15, pady=15, bg="#f2f2f2")
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Listado de Productos Registrados", font=("Arial", 14, "bold"),
             bg="#f2f2f2", fg="#333333").pack(pady=(0, 10))

    columnas = ("ID", "Nombre", "Código", "Stock", "Ubicación", "Proveedor", "Precio")

    tabla = ttk.Treeview(frame, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=110)
    tabla.pack(fill=tk.BOTH, expand=True)

    conn = sqlite3.connect("db/inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, codigo, stock, ubicacion, proveedor, precio FROM productos")
    productos = cursor.fetchall()
    conn.close()

    for producto in productos:
        tabla.insert("", tk.END, values=producto)

    ventana.mainloop()
