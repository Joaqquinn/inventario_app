import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os
from main import mostrar_menu  # Importa la función que muestra el menú principal

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def mostrar_login():
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
            mostrar_menu(nombre_usuario, rol)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    ventana = tk.Tk()
    ventana.title("Login - Maestranzas Unidos S.A.")
    centrar_ventana(ventana, 400, 450)
    ventana.configure(bg="#f2f2f2")

    frame = tk.Frame(ventana, bg="#f2f2f2")
    frame.pack(pady=20)

    # Cargar logo
    ruta_logo = os.path.join("assets", "logo_maestranzas.png")
    if os.path.exists(ruta_logo):
        logo_img = Image.open(ruta_logo)
        logo_img = logo_img.resize((150, 150))
        logo = ImageTk.PhotoImage(logo_img)
        tk.Label(frame, image=logo, bg="#f2f2f2").image = logo  # mantener referencia
        tk.Label(frame, image=logo, bg="#f2f2f2").pack()

    tk.Label(frame, text="Usuario", font=("Arial", 12), bg="#f2f2f2").pack(pady=5)
    entry_usuario = tk.Entry(frame, font=("Arial", 12))
    entry_usuario.pack()

    tk.Label(frame, text="Contraseña", font=("Arial", 12), bg="#f2f2f2").pack(pady=5)
    entry_contraseña = tk.Entry(frame, show="*", font=("Arial", 12))
    entry_contraseña.pack()

    tk.Button(frame, text="Ingresar", font=("Arial", 12), bg="#007ACC", fg="white", command=validar_login).pack(pady=20)

    ventana.mainloop()
    