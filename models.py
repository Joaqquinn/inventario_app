from dataclasses import dataclass

@dataclass
class Item:
    id: int = None
    nombre: str = ''
    descripcion: str = ''
    stock: int = 0
    stock_minimo: int = 0

@dataclass
class Movimiento:
    id: int = None
    item_id: int = None
    cantidad: int = 0
    tipo: str = ''      # 'entrada' o 'salida'
    fecha: str = ''     # ISO-8601
