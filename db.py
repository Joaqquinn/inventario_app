import sqlite3
from datetime import datetime
import shutil

DB_NAME = 'inventory.db'

def init_db():
    """
    Crea las tablas 'items' y 'movimientos' si no existen.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Tabla de ítems
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            stock INTEGER NOT NULL,
            stock_minimo INTEGER NOT NULL
        )
    ''')
    # Tabla de movimientos
    c.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY(item_id) REFERENCES items(id)
        )
    ''')
    conn.commit()
    conn.close()

def ejecutar(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    lastrow = c.lastrowid
    conn.close()
    return lastrow

def consultar(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

def get_movements(item_id):
    """Devuelve lista de (tipo, cantidad, fecha) ordenada por fecha descendente."""
    return consultar(
        "SELECT tipo, cantidad, fecha FROM movimientos WHERE item_id = ? ORDER BY fecha DESC",
        (item_id,)
    )


def backup_db(backup_path):
    """Copia el archivo SQLite a la ruta dada."""
    shutil.copy(DB_NAME, backup_path)

def delete_item(item_id):
    """Elimina un ítem y todos sus movimientos."""
    ejecutar("DELETE FROM movimientos WHERE item_id = ?", (item_id,))
    ejecutar("DELETE FROM items WHERE id = ?", (item_id,))