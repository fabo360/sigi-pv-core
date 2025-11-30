from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Product:
    """
    Representa un producto del inventario.
    """
    code: str
    name: str
    price: float
    stock: int
    location: str


@dataclass
class CartItem:
    """
    Representa una línea en el carrito de venta.
    """
    product_code: str
    quantity: int


class Cart:
    """
    Carrito de venta. Solo contiene lógica de agregación de ítems.
    """
    def __init__(self) -> None:
        self._items: Dict[str, CartItem] = {}

    def add_item(self, product_code: str, quantity: int) -> None:
        """
        Agrega una cantidad al carrito. La validación de cantidad
        y stock se hace en los servicios de dominio.
        """
        if product_code in self._items:
            self._items[product_code].quantity += quantity
        else:
            self._items[product_code] = CartItem(
                product_code=product_code,
                quantity=quantity,
            )

    def get_items(self) -> List[CartItem]:
        return list(self._items.values())

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def clear(self) -> None:
        self._items.clear()
