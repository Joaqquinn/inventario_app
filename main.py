def mostrar_menu(nombre_usuario, rol):
    import tkinter as tk
    from views.product_view import registrar_producto
    from views.movement_view import registrar_movimiento
    from views.alert_view import mostrar_alertas_stock_bajo
    from views.history_view import ver_historial_movimientos
    from views.list_product_view import listar_productos

    def centrar_ventana(ventana, ancho, alto):
        ventana.update_idletasks()
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    menu = tk.Tk()
    menu.title("Menú Principal")
    centrar_ventana(menu, 320, 400)

    frame = tk.Frame(menu, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text=f"Bienvenido, {nombre_usuario} ({rol})", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Button(frame, text="Registrar Producto", font=("Arial", 12), command=registrar_producto).pack(pady=5)
    tk.Button(frame, text="Registrar Movimiento", font=("Arial", 12), command=registrar_movimiento).pack(pady=5)
    tk.Button(frame, text="Ver Productos", font=("Arial", 12), command=listar_productos).pack(pady=5)
    tk.Button(frame, text="Alertas de Stock Bajo", font=("Arial", 12), command=mostrar_alertas_stock_bajo).pack(pady=5)
    tk.Button(frame, text="Ver Historial de Movimientos", font=("Arial", 12), command=ver_historial_movimientos).pack(pady=5)

    menu.mainloop()


# Iniciar app desde login
if __name__ == "__main__":
    from views.login_view import mostrar_login
    mostrar_login()
