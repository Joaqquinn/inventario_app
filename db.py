import sqlite3

# Función para conectar a la base de datos
def conectar():
    conexion = sqlite3.connect('inventario.db')
    return conexion

# Función para crear la tabla de productos (si no existe)
def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            numero_serie TEXT,
            cantidad INTEGER,
            ubicacion TEXT,
            categoria TEXT,
            proveedor TEXT,
            fecha_vencimiento TEXT,
            precio_compra REAL
        )
    ''')
    conn.commit()
    conn.close()

# Función para agregar un nuevo producto
def agregar_producto(nombre, numero_serie, cantidad, ubicacion, categoria, proveedor, fecha_vencimiento, precio_compra):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, numero_serie, cantidad, ubicacion, categoria, proveedor, fecha_vencimiento, precio_compra)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, numero_serie, cantidad, ubicacion, categoria, proveedor, fecha_vencimiento, precio_compra))
    conn.commit()
    conn.close()


# Función para obtener todos los productos
def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return productos

# Función para crear la tabla de movimientos
def crear_tabla_movimientos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            tipo_movimiento TEXT,
            cantidad INTEGER,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    ''')
    conn.commit()
    conn.close()

# Función para registrar un movimiento (entrada o salida)
def registrar_movimiento(producto_id, tipo_movimiento, cantidad):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO movimientos (producto_id, tipo_movimiento, cantidad)
        VALUES (?, ?, ?)
    ''', (producto_id, tipo_movimiento, cantidad))

    # Actualizar cantidad en la tabla productos
    if tipo_movimiento == "entrada":
        cursor.execute('''
            UPDATE productos SET cantidad = cantidad + ? WHERE id = ?
        ''', (cantidad, producto_id))
    elif tipo_movimiento == "salida":
        cursor.execute('''
            UPDATE productos SET cantidad = cantidad - ? WHERE id = ?
        ''', (cantidad, producto_id))

    conn.commit()
    conn.close()

# Función para obtener todos los productos disponibles (para elegir en movimiento)
def obtener_productos_id_nombre():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return productos

# Función para obtener productos con stock bajo
def obtener_productos_stock_bajo(umbral=5):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE cantidad <= ?', (umbral,))
    productos = cursor.fetchall()
    conn.close()
    return productos

