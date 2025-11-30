import os
import sys

# Añadir la carpeta src al path para poder importar core/ e infra/
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from core.models import Product, Cart
from core.services import InventoryService, SaleService
from core.errors import DomainError
from infra.memory_repositories import InMemoryProductRepository, InMemorySaleRepository


def _build_repos_and_services():
    """
    Crea repositorios en memoria, carga productos de ejemplo
    y construye InventoryService + SaleService.
    """
    product_repo = InMemoryProductRepository()
    sale_repo = InMemorySaleRepository()

    # Productos de prueba
    product_repo.save(
        Product(
            code="P001",
            name="Taladro",
            price=50.0,
            stock=10,
            location="Estante B2",
        )
    )
    product_repo.save(
        Product(
            code="P002",
            name="Caja de tornillos",
            price=5.0,
            stock=20,
            location="Estante C3",
        )
    )

    inventory_service = InventoryService(product_repo)
    sale_service = SaleService(product_repo, sale_repo, inventory_service)

    return product_repo, sale_repo, sale_service


def test_confirm_sale_generates_receipt_and_updates_stock():
    """
    confirm_sale debe:
    - Generar un recibo con los ítems correctos
    - Calcular el total correcto
    - Descontar stock en el repositorio de productos
    - Registrar la venta en el repositorio de ventas
    """
    product_repo, sale_repo, sale_service = _build_repos_and_services()

    cart = Cart()
    cart.add_item("P001", 2)  # 2 * 50 = 100
    cart.add_item("P002", 3)  # 3 * 5  = 15

    receipt = sale_service.confirm_sale(cart)

    # Verificar total
    assert receipt.grand_total == 115.0
    assert len(receipt.items) == 2

    # Verificar detalle del primer ítem
    item1 = next(i for i in receipt.items if i.product_code == "P001")
    assert item1.quantity == 2
    assert item1.unit_price == 50.0
    assert item1.total == 100.0

    # Verificar stock actualizado
    p1 = product_repo.find_by_code("P001")
    p2 = product_repo.find_by_code("P002")
    assert p1 is not None and p1.stock == 8   # 10 - 2
    assert p2 is not None and p2.stock == 17  # 20 - 3

    # Verificar que la venta fue registrada
    sales = sale_repo.list_sales()
    assert len(sales) == 1
    assert sales[0]["grand_total"] == 115.0
    assert len(sales[0]["items"]) == 2


def test_confirm_sale_raises_for_empty_cart():
    """
    confirm_sale debe lanzar DomainError si el carrito está vacío.
    """
    _, _, sale_service = _build_repos_and_services()

    cart = Cart()

    with pytest.raises(DomainError):
        sale_service.confirm_sale(cart)


def test_confirm_sale_raises_when_insufficient_stock():
    """
    Si se intenta vender más de lo que hay en stock,
    confirm_sale debe lanzar DomainError.
    """
    _, _, sale_service = _build_repos_and_services()

    cart = Cart()
    # Sabemos que P001 tiene stock 10. Pedimos 999.
    cart.add_item("P001", 999)

    with pytest.raises(DomainError):
        sale_service.confirm_sale(cart)
