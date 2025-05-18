import tkinter as tk
from tkinter import messagebox
import sqlite3

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
        else:  # salida
            cursor.execute("SELECT stock FROM productos WHERE id = ?", (producto_id,))
            stock_actual = cursor.fetchone()[0]
            if cantidad > stock_actual:
                messagebox.showerror("Error", "No hay suficiente stock.")
                conn.close()
                return
            cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad, producto_id))

        # Registrar movimiento
        cursor.execute("""
            INSERT INTO movimientos (producto_id, tipo, cantidad) 
            VALUES (?, ?, ?)
        """, (producto_id, tipo, cantidad))

        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", f"Movimiento de {tipo} registrado.")
        ventana.destroy()

    # Crear ventana
    ventana = tk.Tk()
    ventana.title("Registrar Movimiento")
    ventana.geometry("400x300")

    productos = cargar_productos()

    tk.Label(ventana, text="Selecciona un producto").pack()
    lista_productos = tk.Listbox(ventana, height=6)
    for p in productos:
        lista_productos.insert(tk.END, f"{p[1]} (ID {p[0]})")
    lista_productos.pack()

    tk.Label(ventana, text="Cantidad").pack()
    entry_cantidad = tk.Entry(ventana)
    entry_cantidad.pack()

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Entrada", command=lambda: actualizar_stock('entrada')).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botones, text="Salida", command=lambda: actualizar_stock('salida')).pack(side=tk.LEFT, padx=10)

    ventana.mainloop()
