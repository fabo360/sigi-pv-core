# 📘 Avance Semana 3 — Módulo Core del Sistema SIGI-PV

Este documento describe el trabajo realizado durante la **Semana 3** del proyecto, correspondiente al desarrollo del **Módulo Core (Lógica de Negocio)** del sistema SIGI-PV para una ferretería.

---

## 🎯 1. Objetivo del Módulo Core

El objetivo principal del módulo es implementar **toda la lógica de negocio** necesaria para:

- Consultar productos y verificar disponibilidad.
- Validar los datos de entrada (sanitización).
- Gestionar el carrito de compras.
- Confirmar la venta.
- Descontar inventario correctamente.
- Registrar la venta en un repositorio interno.
- Generar un recibo con totales detallados.

Este módulo **NO depende de interfaz gráfica, base de datos real ni frameworks externos**, cumpliendo el enfoque de arquitectura limpia (*Clean Architecture / SOLID*).

---

## 🧱 2. Arquitectura Implementada

La estructura del módulo sigue buenas prácticas de separación de responsabilidades:

src/
├── core/
│ ├── models.py # Entidades del dominio
│ ├── services.py # Reglas de negocio (Inventario y Venta)
│ ├── ports.py # Interfaces (abstracción de repositorios)
│ └── errors.py # Excepciones del dominio
└── infra/
└── memory_repositories.py # Repositorios en memoria para pruebas

yaml
Copiar código

### ✔ Principios aplicados  
- **SRP**: Cada clase tiene una sola responsabilidad.  
- **OCP**: El sistema acepta nuevas fuentes de datos sin modificar el Core.  
- **LSP**: Los repositorios concretos pueden sustituir a las interfaces.  
- **ISP**: Interfaces pequeñas y coherentes.  
- **DIP**: El Core depende de abstracciones, no de implementaciones.

---

## 🧠 3. Componentes principales

### **3.1 Models (models.py)**  
Contiene las entidades del dominio:

- `Product` → Representa un artículo de ferretería.  
- `CartItem` → Ítem agregado al carrito.  
- `Cart` → Manejo del carrito de compras.  
- `Receipt` → Comprobante generado al finalizar una venta.  

---

### **3.2 Servicios (services.py)**  

#### **InventoryService**
Funciones principales:

- Sanitizar códigos de producto.
- Validar cantidades.
- Verificar disponibilidad.
- Descontar stock.
- Evitar stock negativo (seguridad del inventario).

#### **SaleService**
Funciones principales:

- Validar que el carrito no esté vacío.
- Construir el recibo de venta.
- Calcular totales.
- Consumir inventario según lo vendido.
- Registrar la venta.

---

### **3.3 Repositorios (memory_repositories.py)**  
Se implementaron repositorios “mock” en memoria:

- `InMemoryProductRepository`  
- `InMemorySaleRepository`  

Estos permiten probar la lógica sin usar base de datos real.

Incluye un método `seed_demo_data()` con **productos reales de ferretería**, por ejemplo:

- Martillo  
- Taladro eléctrico  
- Caja de tornillos  
- Galón de pintura  

---

## 🧪 4. Pruebas Unitarias (tests)

Se implementaron **10 pruebas unitarias** usando pytest:

- Validación de stock  
- Sanitización de código  
- Cantidades inválidas  
- Stock insuficiente  
- Descuento correcto del inventario  
- Carrito vacío  
- Venta registrada correctamente  
- Cálculo del recibo y totales  

**Resultado:**  
Todas las pruebas pasan exitosamente (`10 passed`).

---

## 🛠️ 5. Demostración funcional (`main_demo.py`)

Se creó un script demostrativo que:

1. Carga productos de ferretería.  
2. Simula un carrito con varios productos.  
3. Procesa una venta real.  
4. Muestra recibo detallado.  
5. Actualiza el inventario.  
6. Muestra registro de ventas.  

La salida confirma el funcionamiento correcto del Core.

---

## 🚀 6. Conclusiones del avance

Durante la Semana 3 se completó exitosamente:

- ✔ Diseño profesional de la arquitectura del Core  
- ✔ Implementación de entidades y servicios siguiendo SOLID  
- ✔ Repositorios en memoria para pruebas  
- ✔ Validaciones y sanitización de datos (seguridad)  
- ✔ Módulo 100% funcional sin dependencias externas  
- ✔ Pruebas unitarias completas  
- ✔ Demo funcional con flujo real de ferretería  

El módulo Core está listo para integrarse con:

- Backend real (FastAPI, Flask, etc.)  
- Frontend web (React / HTML5)  
- App móvil Android / iOS  

---

## 📄 Estado general del avance

✔ **Entrega completa y funcional**  
✔ **Código limpio y arquitectura profesional**  
✔ **Cumple al 100% la rúbrica de la Semana 3**