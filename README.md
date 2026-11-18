# Food Store - Sistema de Gestión de Pedidos de Comida (Consola)

**Trabajo Práctico Integrador - Programación II**  
**Tecnicatura Universitaria en Programación - UTN**  
**Autores:** Di Lorenzo, Karim / Villalba

---

## 1. Requisitos y Ejecución del Proyecto

* **Versión de Python requerida:** Python 3.12 o superior (utiliza exclusivamente la biblioteca estándar: `abc`, `enum`, `datetime`, `typing`).
* **Ubicación del código fuente:** Carpeta `food_store/`.

### Comandos para ejecutar el sistema interactivo:
```bash
cd food_store
python main.py
```

### Comandos para ejecutar el banco de pruebas automáticas (sin menú):
```bash
cd food_store
python pruebas.py
```

---

## 2. Credenciales Iniciales de Acceso

El sistema precarga automáticamente en `main.py` un usuario con rol **ADMIN**, un usuario cliente (**USUARIO**), categorías, productos y un pedido de ejemplo para facilitar la evaluación inmediata:

| Rol | Mail | Contraseña | Permisos |
| :--- | :--- | :--- | :--- |
| **ADMIN** | `admin@foodstore.com` | `admin123` | Alta, baja lógica, modificación y consulta de Categorías, Productos, Usuarios y Pedidos. |
| **USUARIO** | `juan@cliente.com` | `cliente123` | Consulta de categorías, productos disponibles con stock, sus propios pedidos y sus datos personales. |

---

## 3. Estructura de Paquetes y Arquitectura

```text
food_store/
├── main.py                     # Punto de entrada: inicializa servicios, datos semilla y sesión
├── pruebas.py                  # Pruebas exhaustivas del modelo, servicios y excepciones
├── calculable.py               # Interfaz Calculable (ABC) con calcular_total() -> None
├── entidades/                  # Capa de Modelo (Clases del UML)
│   ├── __init__.py
│   ├── base.py                 # Clase abstracta Base (id, eliminado, creado_en, __eq__, __str__)
│   ├── categoria.py            # Clase Categoria (agregación 1..N con Producto)
│   ├── producto.py             # Clase Producto (asociación N..1 con Categoria)
│   ├── usuario.py              # Clase Usuario (ocultamiento de contraseña, asociación 1..N con Pedido)
│   ├── pedido.py               # Clase Pedido (implementa Calculable, composición 1..N con DetallePedido)
│   └── detalle_pedido.py       # Clase DetallePedido (creada exclusivamente por Pedido)
├── enums/                      # Enumerados del dominio
│   ├── __init__.py
│   ├── rol.py                  # Rol (ADMIN, USUARIO)
│   ├── estado.py               # Estado (PENDIENTE, CONFIRMADO, TERMINADO, CANCELADO)
│   └── forma_pago.py           # FormaPago (TARJETA, TRANSFERENCIA, EFECTIVO)
├── excepciones/                # Jerarquía de excepciones propias
│   ├── __init__.py
│   └── excepciones.py          # FoodStoreError y sus subclases específicas
├── servicios/                  # Capa de Lógica de Negocio y Colecciones en memoria
│   ├── __init__.py
│   ├── categoria_servicio.py   # CategoriaServicio
│   ├── producto_servicio.py    # ProductoServicio
│   ├── usuario_servicio.py     # UsuarioServicio (incluye autenticar())
│   └── pedido_servicio.py      # PedidoServicio (atomicidad de stock y transiciones)
└── consola/                    # Capa de Presentación e Interfaz de Usuario
    ├── __init__.py             # Fábrica polimórfica crear_menu()
    ├── entradas.py             # Funciones de lectura validada por teclado
    ├── menu.py                 # Clase abstracta Menu
    ├── menu_administrador.py   # Subclase MenuAdministrador
    └── menu_cliente.py         # Subclase MenuCliente
```

---

## 4. Enlaces de Entrega

* **Informe Técnico en PDF:** Incluido en la raíz del proyecto (`Informe_TPI_Programacion_II.pdf`).
* **Video Demostración (10-15 min):** 
* **Repositorio GitHub:** (https://github.com/KarimDiLorenzo/TPI-PROG2-DiLorenzo-Villalba-TUP-UTN-FRM.git)
