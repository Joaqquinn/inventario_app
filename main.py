import tkinter as tk
from tkinter import messagebox
import sqlite3
from views.product_view import registrar_producto
from views.movement_view import registrar_movimiento

def validar_login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    conn = sqlite3.connect("db/inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT usuarios.username, roles.nombre 
        FROM usuarios 
        JOIN roles ON usuarios.rol_id = roles.id 
        WHERE usuarios.username = ? AND usuarios.password = ?
    """, (usuario, contraseña))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        nombre_usuario, rol = resultado
        messagebox.showinfo("Login exitoso", f"Bienvenido, {nombre_usuario} ({rol})")
        ventana.destroy()

        menu = tk.Tk()
        menu.title("Menú Principal")
        menu.geometry("300x200")

        tk.Label(menu, text=f"Bienvenido, {nombre_usuario} ({rol})").pack(pady=10)

        tk.Button(menu, text="Registrar Producto", command=registrar_producto).pack(pady=5)
        tk.Button(menu, text="Registrar Movimiento", command=registrar_movimiento).pack(pady=5)

        menu.mainloop()


# Ventana
ventana = tk.Tk()
ventana.title("Login - Inventario Maestranzas Unidos")
ventana.geometry("300x200")

tk.Label(ventana, text="Usuario").pack(pady=5)
entry_usuario = tk.Entry(ventana)
entry_usuario.pack()

tk.Label(ventana, text="Contraseña").pack(pady=5)
entry_contraseña = tk.Entry(ventana, show="*")
entry_contraseña.pack()

tk.Button(ventana, text="Ingresar", command=validar_login).pack(pady=20)

ventana.mainloop()
