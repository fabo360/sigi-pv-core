📘 SIGI-PV – Módulo Core (Lógica de Negocio)

Este repositorio contiene el módulo Core del sistema SIGI-PV, encargado de la lógica de negocio pura del proceso de Venta y Actualización de Inventario en Tiempo Real.

Este módulo está construido siguiendo principios SOLID, Clean Code y sanitización de entrada, de acuerdo con los criterios de evaluación del proyecto.

🧱 Objetivo del Módulo Core

El objetivo es encapsular la lógica del negocio sin depender de:

❌ Interfaz gráfica
❌ Base de datos real
❌ Frameworks externos

✔ Únicamente se implementa la lógica fundamental del negocio, tal como lo exige el avance del proyecto.

📂 Arquitectura del Proyecto
sigi-pv-core/
│
├── src/
│   ├── core/
│   │   ├── models.py            # Entidades del dominio
│   │   ├── services.py          # Lógica de negocio (Inventario y Venta)
│   │   ├── ports.py             # Interfaces de repositorios
│   │   └── errors.py            # Excepciones de dominio y validación
│   │
│   └── infra/
│       └── memory_repositories.py   # Repositorios temporales en memoria
│
├── docs/
│   └── BPMN_Venta_Inventario.png  # Diagrama BPMN del proceso
│
├── .gitignore
└── README.md

🧠 Descripción del Módulo Core

El Core implementa las reglas del negocio para:

Validar existencia y disponibilidad de productos

Validar entrada del usuario (sanitización de código, cantidad, precio)

Agregar productos al carrito

Confirmar la venta

Descontar inventario

Registrar la venta en un repositorio (en memoria, sin BD real)

Generar un recibo interno (objeto) que luego podrá convertirse en ticket/factura

Componentes principales:
1. models.py

Product, CartItem, Cart

Contiene las entidades del dominio

2. services.py

InventoryService: validación de stock y sanitización

SaleService: confirmación de venta, generación de recibo

Funciones cortas y separadas (Clean Code)

3. ports.py

Interfaces abstractas para repositorios

Alineado con Inversión de Dependencias (D de SOLID)

4. memory_repositories.py

Implementaciones temporales en memoria para pruebas

Permite ejecutar el Core sin usar BD real

🚀 Integración futura

El módulo Core está diseñado para permitir la integración con diferentes capas y tecnologías sin modificar la lógica del negocio.

1️⃣ Frontend Web (React / HTML5) – Punto de Venta y Gestión

El Core podrá ser consumido por un frontend moderno mediante API REST:

Navegadores web

Sistemas POS

Interfaces de gestión para empleados de la ferretería

El intercambio se realizará mediante:

👉 HTTPS / JSON
👉 Controladores en el backend que llamen a los servicios del Core

2️⃣ App móvil Android / iOS – Consulta y Conteo de Stock

El sistema también contempla el desarrollo futuro de una aplicación móvil, cuyo propósito será:

👁‍🗨 Consulta rápida de productos

📦 Verificación de stock en tiempo real

🔄 Conteo de inventario para auditorías internas

Esta app se comunicará con el backend usando:

👉 API REST (HTTPS / JSON)
👉 Endpoints conectados al Core mediante los servicios de dominio

3️⃣ Backend Real (FastAPI, Flask, Django, Node.js u otro)

El Core ya está preparado para:

Reemplazar repositorios en memoria por BD real (PostgreSQL / MySQL)

Exponerse mediante controladores / routers

Ser consumido por los frontends (web + móvil)

El patrón utilizado permite agregar funcionalidades sin romper el Core.

📄 Licencia

Proyecto académico — Uso educativo.