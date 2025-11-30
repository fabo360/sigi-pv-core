from dataclasses import dataclass
from typing import List
from .models import Product, Cart, CartItem
from .ports import ProductRepository, SaleRepository
from .errors import DomainError, ValidationError


# ==========
# Sanitización básica de entradas
# ==========

_MAX_CODE_LENGTH = 50
_MAX_NAME_LENGTH = 100


def _sanitize_product_code(code: str) -> str:
    if not isinstance(code, str):
        raise ValidationError("El código de producto debe ser texto.")
    code = code.strip()
    if not code:
        raise ValidationError("El código de producto no puede estar vacío.")
    if len(code) > _MAX_CODE_LENGTH:
        raise ValidationError("El código de producto es demasiado largo.")
    return code


def _sanitize_quantity(quantity: int) -> int:
    if not isinstance(quantity, int):
        raise ValidationError("La cantidad debe ser un número entero.")
    if quantity <= 0:
        raise ValidationError("La cantidad debe ser mayor a cero.")
    return quantity


def _sanitize_price(price: float) -> float:
    if price is None:
        raise ValidationError("El precio no puede ser nulo.")
    if price < 0:
        raise ValidationError("El precio del producto no puede ser negativo.")
    return price


# ==========
# Objetos de recibo
# ==========

@dataclass
class ReceiptItem:
    product_code: str
    name: str
    quantity: int
    unit_price: float
    total: float


@dataclass
class Receipt:
    items: List[ReceiptItem]
    grand_total: float


# ==========
# Servicios de dominio
# ==========


class InventoryService:
    """
    Lógica de inventario: validación y descuento de stock.
    """

    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo

    def check_availability(self, product_code: str, quantity: int) -> Product:
        """
        Verifica que el producto exista, que el código sea válido,
        que la cantidad sea positiva y que haya stock suficiente.
        """
        clean_code = _sanitize_product_code(product_code)
        clean_quantity = _sanitize_quantity(quantity)

        product = self._product_repo.find_by_code(clean_code)
        if product is None:
            raise DomainError("El producto solicitado no existe en el inventario.")

        product.price = _sanitize_price(product.price)

        if product.stock < clean_quantity:
            raise DomainError("Stock insuficiente para la cantidad solicitada.")

        return product

    def discount_stock(self, item: CartItem) -> None:
        """
        Descuenta del stock la cantidad vendida. Vuelve a validar
        para asegurar que el stock no quede negativo.
        """
        product_code = _sanitize_product_code(item.product_code)
        clean_quantity = _sanitize_quantity(item.quantity)

        product = self._product_repo.find_by_code(product_code)
        if product is None:
            raise DomainError("El producto no existe al intentar descontar stock.")

        new_stock = product.stock - clean_quantity
        if new_stock < 0:
            raise DomainError("La operación dejaría el stock en negativo.")

        product.stock = new_stock
        self._product_repo.save(product)


class SaleService:
    """
    Lógica de venta: valida el carrito, descuenta stock,
    registra la venta y genera un recibo.
    """

    def __init__(
        self,
        product_repo: ProductRepository,
        sale_repo: SaleRepository,
        inventory_service: InventoryService,
    ) -> None:
        self._product_repo = product_repo
        self._sale_repo = sale_repo
        self._inventory_service = inventory_service

    def confirm_sale(self, cart: Cart) -> Receipt:
        """
        Punto de entrada principal del módulo Core para confirmar una venta.
        """
        self._validate_cart_not_empty(cart)

        receipt_items = self._build_receipt_items(cart)
        grand_total = sum(item.total for item in receipt_items)

        self._apply_stock_discount(cart)
        self._register_sale(receipt_items, grand_total)

        return Receipt(items=receipt_items, grand_total=grand_total)

    # ----- Métodos privados (Clean Code: funciones cortas) -----

    @staticmethod
    def _validate_cart_not_empty(cart: Cart) -> None:
        if cart.is_empty():
            raise DomainError("El carrito está vacío. No se puede confirmar la venta.")

    def _build_receipt_items(self, cart: Cart) -> List[ReceiptItem]:
        """
        Valida disponibilidad de cada ítem del carrito y construye
        las líneas del recibo.
        """
        receipt_items: List[ReceiptItem] = []

        for item in cart.get_items():
            product = self._inventory_service.check_availability(
                item.product_code,
                item.quantity,
            )

            line_total = product.price * item.quantity
            receipt_items.append(
                ReceiptItem(
                    product_code=product.code,
                    name=self._sanitize_name_for_receipt(product.name),
                    quantity=item.quantity,
                    unit_price=product.price,
                    total=line_total,
                )
            )

        return receipt_items

    def _apply_stock_discount(self, cart: Cart) -> None:
        """
        Descuenta del inventario todas las cantidades del carrito.
        """
        for item in cart.get_items():
            self._inventory_service.discount_stock(item)

    def _register_sale(self, receipt_items: List[ReceiptItem], grand_total: float) -> None:
        """
        Registra la venta en el repositorio de ventas.
        """
        sale_payload = {
            "items": [
                {
                    "product_code": i.product_code,
                    "name": i.name,
                    "quantity": i.quantity,
                    "unit_price": i.unit_price,
                    "total": i.total,
                }
                for i in receipt_items
            ],
            "grand_total": grand_total,
        }
        self._sale_repo.save_sale(sale_payload)

    @staticmethod
    def _sanitize_name_for_receipt(name: str) -> str:
        """
        Sanitiza el nombre del producto que se mostrará en el recibo.
        (Defensa adicional ante nombres muy largos o con espacios raros)
        """
        if not isinstance(name, str):
            return "Producto sin nombre"
        clean = name.strip()
        if not clean:
            return "Producto sin nombre"
        return clean[:_MAX_NAME_LENGTH]
