import tkinter as tk
from tkinter import messagebox
import sqlite3
from utils.style import aplicar_estilos_generales

def registrar_movimiento():
    def cargar_productos():
        conn = sqlite3.connect("db/inventario.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM productos")
        productos = cursor.fetchall()
        conn.close()
        return productos

    def actualizar_stock(tipo):
        producto_index = lista_productos.curselection()
        if not producto_index:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return

        producto = productos[producto_index[0]]
        producto_id = producto[0]
        cantidad = entry_cantidad.get()

        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Cantidad inválida.")
            return

        cantidad = int(cantidad)
        conn = sqlite3.connect("db/inventario.db")
        cursor = conn.cursor()

        if tipo == 'entrada':
            cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (cantidad, producto_id))
        else:
            cursor.execute("SELECT stock FROM productos WHERE id = ?", (producto_id,))
            stock_actual = cursor.fetchone()[0]
            if cantidad > stock_actual:
                messagebox.showerror("Error", "No hay suficiente stock.")
                conn.close()
                return
            cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad, producto_id))

        cursor.execute("INSERT INTO movimientos (producto_id, tipo, cantidad) VALUES (?, ?, ?)",
                       (producto_id, tipo, cantidad))

        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", f"Movimiento de {tipo} registrado.")
        ventana.destroy()

    def centrar_ventana(ventana, ancho, alto):
        ventana.update_idletasks()
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    ventana = tk.Tk()
    ventana.title("Registrar Movimiento")
    centrar_ventana(ventana, 500, 450)
    ventana.configure(bg="#f2f2f2")

    aplicar_estilos_generales()

    frame = tk.Frame(ventana, padx=20, pady=20, bg="#f2f2f2")
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Selecciona un producto", font=("Arial", 12), bg="#f2f2f2").pack(pady=5)
    lista_productos = tk.Listbox(frame, height=6, font=("Arial", 11))
    productos = cargar_productos()
    for p in productos:
        lista_productos.insert(tk.END, f"{p[1]} (ID {p[0]})")
    lista_productos.pack(pady=5)

    tk.Label(frame, text="Cantidad", font=("Arial", 12), bg="#f2f2f2").pack(pady=5)
    entry_cantidad = tk.Entry(frame, font=("Arial", 12))
    entry_cantidad.pack(pady=5)

    btn_frame = tk.Frame(frame, bg="#f2f2f2")
    btn_frame.pack(pady=15)

    tk.Button(btn_frame, text="Entrada", font=("Arial", 12), bg="#007ACC", fg="white",
              command=lambda: actualizar_stock('entrada')).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Salida", font=("Arial", 12), bg="#007ACC", fg="white",
              command=lambda: actualizar_stock('salida')).pack(side=tk.LEFT, padx=10)

    ventana.mainloop()
