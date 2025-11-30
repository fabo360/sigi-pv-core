import os
import sys

# Añadir la carpeta src al path para poder importar core/ e infra/
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from core.models import Product
from core.services import InventoryService
from core.errors import DomainError, ValidationError
from infra.memory_repositories import InMemoryProductRepository


def _build_repo_with_sample_product() -> InMemoryProductRepository:
    """
    Crea un repositorio en memoria con un producto de ejemplo.
    """
    repo = InMemoryProductRepository()
    product = Product(
        code="P001",
        name="Martillo 16oz",
        price=10.0,
        stock=5,
        location="Estante A1",
    )
    repo.save(product)
    return repo


def test_check_availability_ok():
    """
    Debe devolver el producto cuando hay stock suficiente
    y los datos de entrada son válidos.
    """
    repo = _build_repo_with_sample_product()
    service = InventoryService(repo)

    product = service.check_availability("P001", 2)

    assert product.code == "P001"
    assert product.stock == 5
    assert product.price == 10.0


def test_check_availability_raises_for_non_existing_product():
    """
    Debe lanzar DomainError cuando el producto no existe.
    """
    repo = InMemoryProductRepository()
    service = InventoryService(repo)

    with pytest.raises(DomainError):
        service.check_availability("NO_EXISTE", 1)


def test_check_availability_raises_for_invalid_quantity():
    """
    Debe lanzar ValidationError cuando la cantidad es <= 0.
    """
    repo = _build_repo_with_sample_product()
    service = InventoryService(repo)

    with pytest.raises(ValidationError):
        service.check_availability("P001", 0)

    with pytest.raises(ValidationError):
        service.check_availability("P001", -3)


def test_check_availability_raises_for_insufficient_stock():
    """
    Debe lanzar DomainError cuando no hay stock suficiente.
    """
    repo = _build_repo_with_sample_product()
    service = InventoryService(repo)

    # Stock = 5, pedimos 10
    with pytest.raises(DomainError):
        service.check_availability("P001", 10)


def test_check_availability_sanitizes_product_code():
    """
    Debe sanitizar el código de producto (espacios extra).
    """
    repo = _build_repo_with_sample_product()
    service = InventoryService(repo)

    # En el repo está guardado como "P001", pero consultamos con espacios
    product = service.check_availability("  P001  ", 1)

    assert product.code == "P001"


def test_discount_stock_updates_repository():
    """
    discount_stock debe disminuir el stock correctamente en el repositorio.
    """
    repo = _build_repo_with_sample_product()
    service = InventoryService(repo)

    # Verificamos estado inicial
    original = repo.find_by_code("P001")
    assert original is not None
    assert original.stock == 5

    # Creamos un CartItem manualmente
    from core.models import CartItem

    item = CartItem(product_code="P001", quantity=2)

    service.discount_stock(item)

    updated = repo.find_by_code("P001")
    assert updated is not None
    assert updated.stock == 3  # 5 - 2


def test_discount_stock_raises_if_stock_would_be_negative():
    """
    Debe lanzar DomainError si la operación dejaría stock negativo.
    """
    repo = _build_repo_with_sample_product()
    service = InventoryService(repo)

    from core.models import CartItem

    item = CartItem(product_code="P001", quantity=999)  # mucho mayor al stock

    with pytest.raises(DomainError):
        service.discount_stock(item)
