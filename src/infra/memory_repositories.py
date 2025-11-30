from typing import Dict, Optional, List
from core.models import Product
from core.ports import ProductRepository, SaleRepository


class InMemoryProductRepository(ProductRepository):
    """
    Implementación en memoria del repositorio de productos.
    Útil para pruebas y para este avance sin BD real.
    """

    def __init__(self) -> None:
        self._data: Dict[str, Product] = {}

    def find_by_code(self, code: str) -> Optional[Product]:
        return self._data.get(code)

    def save(self, product: Product) -> None:
        self._data[product.code] = product

    def list_all(self) -> List[Product]:
        return list(self._data.values())

    def seed_demo_data(self) -> None:
        """
        Carga algunos productos de ejemplo para pruebas manuales.
        """
        self.save(
            Product(
                code="H001",
                name="Martillo 16 oz mango fibra",
                price=9.5,
                stock=25,
                location="Pasillo 1 - Herramientas de mano",
            )
        )
        self.save(
            Product(
                code="D001",
                name="Taladro eléctrico 600W",
                price=49.9,
                stock=10,
                location="Pasillo 2 - Herramientas eléctricas",
            )
        )
        self.save(
            Product(
                code="T001",
                name="Caja de tornillos 1/4\" x 100 und",
                price=5.2,
                stock=40,
                location="Pasillo 3 - Tornillería",
            )
        )
        self.save(
            Product(
                code="P001",
                name="Galón de pintura blanca interior",
                price=18.0,
                stock=15,
                location="Pasillo 4 - Pinturas",
            )
        )

class InMemorySaleRepository(SaleRepository):
    """
    Implementación en memoria del repositorio de ventas.
    Permite verificar que la venta se registró sin usar BD real.
    """

    def __init__(self) -> None:
        self._sales: List[dict] = []

    def save_sale(self, data: dict) -> None:
        self._sales.append(data)

    def list_sales(self) -> List[dict]:
        return list(self._sales)
