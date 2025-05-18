import tkinter as tk
from tkinter import messagebox
import sqlite3
from utils.style import aplicar_estilos_generales  # Usamos estilos comunes

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

    def centrar_ventana(ventana, ancho, alto):
        ventana.update_idletasks()
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    ventana = tk.Tk()
    ventana.title("Registro de Producto")
    centrar_ventana(ventana, 500, 500)
    ventana.configure(bg="#f2f2f2")

    aplicar_estilos_generales()  # Aplicar estilos para tablas, botones, etc.

    frame = tk.Frame(ventana, padx=20, pady=20, bg="#f2f2f2")
    frame.pack(fill=tk.BOTH, expand=True)

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

    global_vars = globals()

    for label, var in campos:
        tk.Label(frame, text=label, font=("Arial", 12), bg="#f2f2f2").pack(pady=3)
        global_vars[var] = tk.Entry(frame, font=("Arial", 12))
        global_vars[var].pack(pady=3)

    tk.Button(frame, text="Guardar", font=("Arial", 12), bg="#007ACC", fg="white", command=guardar).pack(pady=20)

    ventana.mainloop()
