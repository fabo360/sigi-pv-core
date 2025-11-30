from abc import ABC, abstractmethod
from typing import Optional, List
from .models import Product


class ProductRepository(ABC):
    """
    Puerto (interfaz) para acceso a productos.
    Implementaciones futuras pueden usar BD real, API, etc.
    """

    @abstractmethod
    def find_by_code(self, code: str) -> Optional[Product]:
        ...

    @abstractmethod
    def save(self, product: Product) -> None:
        ...

    @abstractmethod
    def list_all(self) -> List[Product]:
        ...


class SaleRepository(ABC):
    """
    Puerto (interfaz) para registrar ventas.
    """
    @abstractmethod
    def save_sale(self, data: dict) -> None:
        ...
