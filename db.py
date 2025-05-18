import sqlite3
import os

# Crear carpeta db si no existe
os.makedirs("db", exist_ok=True)

# Conectar a la base de datos SQLite
conn = sqlite3.connect("db/inventario.db")
cursor = conn.cursor()

# Crear tabla de roles
cursor.execute("""
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
)
""")

# Crear tabla de usuarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    rol_id INTEGER,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
)
""")

# Insertar roles
roles = ['Administrador', 'Gestor de Inventario', 'Comprador', 'Trabajador de Planta']
for rol in roles:
    cursor.execute("INSERT OR IGNORE INTO roles (nombre) VALUES (?)", (rol,))

# Insertar un usuario de prueba
cursor.execute("INSERT OR IGNORE INTO usuarios (username, password, rol_id) VALUES (?, ?, ?)",
               ("admin", "admin123", 1))

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    codigo TEXT UNIQUE,
    stock INTEGER DEFAULT 0,
    proveedor TEXT,
    ubicacion TEXT,
    precio REAL,
    stock_minimo INTEGER DEFAULT 0
)
""")

# Crear tabla de movimientos
cursor.execute("""
CREATE TABLE IF NOT EXISTS movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER,
    tipo TEXT CHECK(tipo IN ('entrada', 'salida')),
    cantidad INTEGER NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
)
""")
# Guardar y cerrar
conn.commit()
conn.close()
