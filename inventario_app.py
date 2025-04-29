import tkinter as tk
from tkinter import messagebox
import db

# Función para centrar ventanas
def centrar_ventana(ventana, ancho=600, alto=400):
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Crear la ventana principal
root = tk.Tk()
root.title("EL 7")
root.configure(bg="#f0f0f0")
centrar_ventana(root, 600, 400)

# Crear tablas si no existen
db.crear_tabla()
db.crear_tabla_movimientos()

# Funciones
def registrar_producto():
    ventana = tk.Toplevel()
    ventana.title("Registrar Producto")
    ventana.configure(bg="#f0f0f0")
    centrar_ventana(ventana, 500, 600)

    # Campos de entrada
    campos = {
        "Nombre del Producto": None,
        "Número de Serie": None,
        "Cantidad": None,
        "Ubicación": None,
        "Categoría": None,
        "Proveedor": None,
        "Fecha de Vencimiento (YYYY-MM-DD)": None,
        "Precio de Compra": None
    }

    entradas = {}

    for campo in campos:
        tk.Label(ventana, text=campo, bg="#f0f0f0", font=("Arial", 10)).pack(pady=5)
        entry = tk.Entry(ventana)
        entry.pack()
        entradas[campo] = entry

    import datetime

    def guardar():
        nombre = entradas["Nombre del Producto"].get()
        numero_serie = entradas["Número de Serie"].get()
        cantidad = entradas["Cantidad"].get()
        ubicacion = entradas["Ubicación"].get()
        categoria = entradas["Categoría"].get()
        proveedor = entradas["Proveedor"].get()
        fecha_vencimiento = entradas["Fecha de Vencimiento (YYYY-MM-DD)"].get()
        precio_compra = entradas["Precio de Compra"].get()

        # Validaciones básicas
        if not nombre or not cantidad:
            messagebox.showerror("Error", "Debes completar al menos el nombre y la cantidad.")
            return

        try:
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        # Validar formato de fecha
        if fecha_vencimiento:
            try:
                datetime.datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "La fecha de vencimiento debe tener formato YYYY-MM-DD.")
                return

        # Validar precio de compra (opcional)
        if precio_compra:
            try:
                precio_compra = float(precio_compra)
            except ValueError:
                messagebox.showerror("Error", "El precio de compra debe ser un número válido.")
                return
        else:
            precio_compra = None

        # Guardar en la base de datos
        db.agregar_producto(
            nombre, numero_serie, cantidad, ubicacion,
            categoria, proveedor, fecha_vencimiento, precio_compra
        )
        messagebox.showinfo("Éxito", "Producto registrado correctamente.")
        ventana.destroy()

    tk.Button(ventana, text="Guardar Producto", command=guardar, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=20)

def ver_inventario():
    ventana = tk.Toplevel()
    ventana.title("Inventario Actual")
    ventana.configure(bg="#f0f0f0")
    centrar_ventana(ventana, 900, 500)  # Más ancho porque hay más columnas

    productos = db.obtener_productos()

    # Nuevos encabezados
    encabezados = [
        "ID", "Nombre", "Número de Serie", "Cantidad", "Ubicación",
        "Categoría", "Proveedor", "Fecha de Vencimiento", "Precio de Compra"
    ]

    # Crear encabezados
    for i, encabezado in enumerate(encabezados):
        label = tk.Label(ventana, text=encabezado, font=('Arial', 10, 'bold'), bg="#f0f0f0")
        label.grid(row=0, column=i, padx=5, pady=5)

    # Llenar tabla con productos
    for fila, producto in enumerate(productos, start=1):
        for columna, dato in enumerate(producto):
            label = tk.Label(ventana, text=str(dato), bg="#f0f0f0", wraplength=120)
            label.grid(row=fila, column=columna, padx=5, pady=5)

def movimientos():
    ventana = tk.Toplevel()
    ventana.title("Registrar Movimiento de Inventario")
    ventana.configure(bg="#f0f0f0")
    centrar_ventana(ventana, 400, 300)

    productos = db.obtener_productos_id_nombre()

    if not productos:
        messagebox.showwarning("Advertencia", "No hay productos registrados.")
        ventana.destroy()
        return

    tk.Label(ventana, text="Producto", bg="#f0f0f0", font=("Arial", 10)).pack(pady=5)

    producto_nombres = [p[1] for p in productos]
    producto_ids = [p[0] for p in productos]

    producto_var = tk.StringVar(ventana)
    producto_var.set(producto_nombres[0])
    dropdown = tk.OptionMenu(ventana, producto_var, *producto_nombres)
    dropdown.pack()

    tk.Label(ventana, text="Tipo de Movimiento", bg="#f0f0f0", font=("Arial", 10)).pack(pady=5)
    tipo_var = tk.StringVar()
    tipo_var.set("entrada")
    tk.OptionMenu(ventana, tipo_var, "entrada", "salida").pack()

    tk.Label(ventana, text="Cantidad", bg="#f0f0f0", font=("Arial", 10)).pack(pady=5)
    entry_cantidad = tk.Entry(ventana)
    entry_cantidad.pack()

    def guardar_movimiento():
        nombre_seleccionado = producto_var.get()
        try:
            index = producto_nombres.index(nombre_seleccionado)
            producto_id = producto_ids[index]
            tipo = tipo_var.get()
            cantidad = entry_cantidad.get()

            if cantidad:
                try:
                    cantidad = int(cantidad)
                    if cantidad <= 0:
                        messagebox.showerror("Error", "La cantidad debe ser mayor a cero.")
                        return
                    db.registrar_movimiento(producto_id, tipo, cantidad)
                    messagebox.showinfo("Éxito", "Movimiento registrado exitosamente.")
                    ventana.destroy()
                except ValueError:
                    messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            else:
                messagebox.showerror("Error", "Debes ingresar una cantidad.")
        except ValueError:
            messagebox.showerror("Error", "Producto no encontrado.")

    tk.Button(ventana, text="Guardar Movimiento", command=guardar_movimiento, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=20)

def alertas_stock():
    ventana = tk.Toplevel()
    ventana.title("Alertas de Stock Bajo")
    ventana.configure(bg="#f0f0f0")
    centrar_ventana(ventana, 600, 400)

    productos = db.obtener_productos_stock_bajo()

    if not productos:
        tk.Label(ventana, text="No hay productos con stock bajo.", font=('Arial', 12), bg="#f0f0f0").pack(pady=20)
        return

    encabezados = ["ID", "Nombre", "Número de Serie", "Cantidad", "Ubicación"]
    for i, encabezado in enumerate(encabezados):
        label = tk.Label(ventana, text=encabezado, font=('Arial', 10, 'bold'), bg="#f0f0f0")
        label.grid(row=0, column=i, padx=10, pady=5)

    for fila, producto in enumerate(productos, start=1):
        for columna, dato in enumerate(producto):
            label = tk.Label(ventana, text=str(dato), bg="#f0f0f0")
            label.grid(row=fila, column=columna, padx=10, pady=5)

# Crear los botones principales
btn_registrar = tk.Button(root, text="Registrar Producto", width=30, height=2, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=registrar_producto)
btn_inventario = tk.Button(root, text="Ver Inventario", width=30, height=2, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=ver_inventario)
btn_movimientos = tk.Button(root, text="Registrar Movimiento", width=30, height=2, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=movimientos)
btn_alertas = tk.Button(root, text="Ver Alertas de Stock", width=30, height=2, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=alertas_stock)

# Posicionar los botones
btn_registrar.pack(pady=10)
btn_inventario.pack(pady=10)
btn_movimientos.pack(pady=10)
btn_alertas.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
