"""
Demostración del módulo Core de SIGI-PV para una FERRETERÍA.
NO usa BD real ni interfaz gráfica.
"""

import os
import sys

# Agregar la carpeta "src" al PYTHONPATH (igual que en los tests)
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from core.models import Cart
from core.services import InventoryService, SaleService
from infra.memory_repositories import (
    InMemoryProductRepository,
    InMemorySaleRepository,
)


def main():
    print("\n=========== DEMO: SIGI-PV Core (Ferretería) ===========")

    # =======================================================
    # 1. Crear repositorios en memoria
    # =======================================================
    product_repo = InMemoryProductRepository()
    sale_repo = InMemorySaleRepository()

    # Cargar datos de ejemplo (ferretería)
    product_repo.seed_demo_data()

    print("\n📦 Productos de ferretería cargados:")
    for p in product_repo.list_all():
        print(f"- {p.code} | {p.name} | ${p.price} | Stock: {p.stock} | {p.location}")

    # =======================================================
    # 2. Crear servicios del Core
    # =======================================================
    inventory_service = InventoryService(product_repo)
    sale_service = SaleService(product_repo, sale_repo, inventory_service)

    # =======================================================
    # 3. Crear un carrito y agregar productos
    # =======================================================
    cart = Cart()
    cart.add_item("H001", 1)   # Martillo
    cart.add_item("D001", 1)   # Taladro
    cart.add_item("T001", 3)   # 3 cajas de tornillos

    print("\n🛒 Carrito creado con los siguientes productos:")
    for item in cart.get_items():
        print(f"- {item.product_code}: {item.quantity} unidad(es)")

    # =======================================================
    # 4. Confirmar la venta
    # =======================================================
    print("\n💰 Procesando venta...")

    receipt = sale_service.confirm_sale(cart)

    print("\n=========== RECIBO (Ferretería) ===========")
    for item in receipt.items:
        print(f"{item.quantity} x {item.name} (${item.unit_price}) = ${item.total}")
    print("-------------------------------------------")
    print(f"TOTAL A PAGAR: ${receipt.grand_total}")
    print("===========================================")

    # =======================================================
    # 5. Ver stock actualizado
    # =======================================================
    print("\n📉 Stock actualizado después de la venta:")
    for p in product_repo.list_all():
        print(f"- {p.code} | {p.name} → Stock: {p.stock}")

    # =======================================================
    # 6. Ventas registradas
    # =======================================================
    print("\n📝 Registro de ventas en memoria:")
    for sale in sale_repo.list_sales():
        print(sale)

    print("\n=========== FIN DE DEMO (Ferretería) ===========\n")


if __name__ == "__main__":
    main()

