import tkinter as tk
from tkinter import messagebox
import sqlite3

def registrar_producto():
    def guardar():
        datos = (
            entry_nombre.get(),
            entry_descripcion.get(),
            entry_codigo.get(),
            entry_stock.get(),
            entry_proveedor.get(),
            entry_ubicacion.get(),
            entry_precio.get(),
            entry_stock_minimo.get()
        )

        conn = sqlite3.connect("db/inventario.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos 
            (nombre, descripcion, codigo, stock, proveedor, ubicacion, precio, stock_minimo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, datos)
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Producto registrado correctamente")
        ventana.destroy()

    ventana = tk.Tk()
    ventana.title("Registro de Producto")
    ventana.geometry("400x400")

    campos = [
        ("Nombre", 'entry_nombre'),
        ("Descripción", 'entry_descripcion'),
        ("Código", 'entry_codigo'),
        ("Stock Inicial", 'entry_stock'),
        ("Proveedor", 'entry_proveedor'),
        ("Ubicación", 'entry_ubicacion'),
        ("Precio", 'entry_precio'),
        ("Stock Mínimo", 'entry_stock_minimo'),
    ]

    for label, var in campos:
        tk.Label(ventana, text=label).pack()
        globals()[var] = tk.Entry(ventana)
        globals()[var].pack()

    tk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)
    ventana.mainloop()
