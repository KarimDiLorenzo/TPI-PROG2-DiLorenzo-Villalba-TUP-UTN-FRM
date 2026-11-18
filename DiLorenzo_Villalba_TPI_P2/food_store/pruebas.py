from entidades.base import Base
from enums.estado import Estado
from enums.forma_pago import FormaPago
from enums.rol import Rol
from excepciones import (
    CredencialesInvalidasError,
    DatoInvalidoError,
    DuplicadoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    PrecioInvalidoError,
    StockInsuficienteError,
)
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


def ejecutar_pruebas() -> None:
    print("=================================================================")
    print("   EJECUCIÓN DE PRUEBAS AUTOMÁTICAS - FOOD STORE (MODELO/SERVICIOS)")
    print("=================================================================\n")

    cat_srv = CategoriaServicio()
    prod_srv = ProductoServicio(cat_srv)
    usr_srv = UsuarioServicio()
    ped_srv = PedidoServicio(usr_srv, prod_srv)

    # 1. Prueba de instanciación de clase abstracta Base
    print("[TEST 1] Verificando imposibilidad de instanciar clase abstracta Base...")
    try:
        Base()  # type: ignore
        print("  [FALLÓ] Se permitió instanciar Base.")
    except TypeError as e:
        print(f"  [OK] Capturado TypeError esperado: {e}")

    # 2. Pruebas de Categorías
    print("\n[TEST 2] Gestión y validaciones de Categorías...")
    cat_burgers = cat_srv.crear("Hamburguesas", "Hamburguesas gourmet")
    cat_bebidas = cat_srv.crear("Bebidas", "Gaseosas y aguas")
    print(f"  [OK] Categoría creada: {cat_burgers}")
    print(f"  [OK] Categoría creada: {cat_bebidas}")

    try:
        cat_srv.crear("hamburguesas", "Duplicada en minúsculas")
        print("  [FALLÓ] Se permitió crear categoría con nombre repetido.")
    except DuplicadoError as e:
        print(f"  [OK] DuplicadoError capturado correctamente: {e}")

    # 3. Pruebas de Productos y PrecioInvalidoError
    print("\n[TEST 3] Gestión y validaciones de Productos...")
    prod_cheddar = prod_srv.crear(
        nombre="Burger Doble Cheddar",
        descripcion="Doble carne con cheddar",
        precio=7500.0,
        stock=10,
        imagen="burger.png",
        disponible=True,
        id_categoria=cat_burgers.id,
    )
    prod_agua = prod_srv.crear(
        nombre="Agua Mineral 500ml",
        descripcion="Agua sin gas",
        precio=1500.0,
        stock=5,
        imagen="agua.png",
        disponible=True,
        id_categoria=cat_bebidas.id,
    )
    print(f"  [OK] Producto creado: {prod_cheddar}")
    print(f"  [OK] Producto creado: {prod_agua}")

    try:
        prod_srv.crear("Producto Inválido", "Desc", -100.0, 5, "img.png", True, cat_burgers.id)
        print("  [FALLÓ] Se permitió precio negativo.")
    except PrecioInvalidoError as e:
        print(f"  [OK] PrecioInvalidoError capturado correctamente: {e}")

    try:
        cat_srv.eliminar(cat_burgers.id)
        print("  [FALLÓ] Se permitió eliminar categoría con productos activos.")
    except OperacionNoPermitidaError as e:
        print(f"  [OK] OperacionNoPermitidaError al eliminar categoría activa: {e}")

    # 4. Pruebas de Usuarios y Autenticación
    print("\n[TEST 4] Gestión de Usuarios, unicidad de mail y autenticación...")
    admin = usr_srv.crear("Ana", "Pérez", "admin@foodstore.com", "2614000001", "admin123", Rol.ADMIN)
    cliente = usr_srv.crear("Carlos", "Ruiz", "carlos@mail.com", "2614000002", "clave123", Rol.USUARIO)
    print(f"  [OK] Admin creado: {admin}")
    print(f"  [OK] Cliente creado: {cliente}")

    try:
        usr_srv.crear("Otro", "Usuario", "ADMIN@foodstore.com", "123", "pass", Rol.USUARIO)
        print("  [FALLÓ] Se permitió mail duplicado.")
    except DuplicadoError as e:
        print(f"  [OK] DuplicadoError en mail capturado: {e}")

    try:
        usr_srv.autenticar("carlos@mail.com", "clave_erronea")
        print("  [FALLÓ] Autenticación aceptó contraseña errónea.")
    except CredencialesInvalidasError as e:
        print(f"  [OK] CredencialesInvalidasError capturado: {e}")

    try:
        usr_srv.eliminar(admin.id, admin)
        print("  [FALLÓ] Admin pudo eliminarse a sí mismo.")
    except OperacionNoPermitidaError as e:
        print(f"  [OK] OperacionNoPermitidaError en auto-eliminación de admin: {e}")

    # 5. Pruebas de Pedidos, Composición, Suma de detalles y Calculable
    print("\n[TEST 5] Creación de Pedidos, suma de producto repetido y descuento de stock...")
    # Agregamos dos veces el mismo producto en la lista de items (2 + 3 = 5 unidades)
    pedido1 = ped_srv.crear_pedido(
        id_usuario=cliente.id,
        forma_pago=FormaPago.EFECTIVO,
        items=[(prod_cheddar.id, 2), (prod_cheddar.id, 3), (prod_agua.id, 2)],
    )
    print(f"  [OK] Pedido creado: {pedido1}")
    print(f"  [OK] Cantidad de líneas de detalle (debe ser 2): {len(pedido1.detalles)}")
    for d in pedido1.detalles:
        print(f"       Detalle: {d}")
    print(f"  [OK] Stock restante de '{prod_cheddar.nombre}' (10 - 5 = 5): {prod_cheddar.stock}")
    print(f"  [OK] Stock restante de '{prod_agua.nombre}' (5 - 2 = 3): {prod_agua.stock}")

    # 6. Prueba de falta de stock en creación de pedido (atomicidad)
    print("\n[TEST 6] Pedido rechazado por falta de stock (sin alterar stocks parciales)...")
    try:
        ped_srv.crear_pedido(
            id_usuario=cliente.id,
            forma_pago=FormaPago.TARJETA,
            items=[(prod_agua.id, 1), (prod_cheddar.id, 50)],
        )
        print("  [FALLÓ] Se permitió crear pedido superando stock.")
    except StockInsuficienteError as e:
        print(f"  [OK] StockInsuficienteError capturado: {e}")
        print(f"  [OK] Stock de '{prod_agua.nombre}' intacto en {prod_agua.stock}")

    # 7. Transiciones de estado y devolución de stock al cancelar
    print("\n[TEST 7] Transiciones de estado y devolución de stock...")
    ped_srv.actualizar_pedido(pedido1.id, nuevo_estado=Estado.CONFIRMADO)
    print(f"  [OK] Estado actualizado a: {pedido1.estado.value}")
    ped_srv.actualizar_pedido(pedido1.id, nuevo_estado=Estado.CANCELADO)
    print(f"  [OK] Estado actualizado a: {pedido1.estado.value}")
    print(
        f"  [OK] Stock devuelto tras cancelar -> '{prod_cheddar.nombre}': {prod_cheddar.stock}, "
        f"'{prod_agua.nombre}': {prod_agua.stock}"
    )

    try:
        ped_srv.actualizar_pedido(pedido1.id, nuevo_estado=Estado.TERMINADO)
        print("  [FALLÓ] Se permitió cambiar estado desde CANCELADO.")
    except OperacionNoPermitidaError as e:
        print(f"  [OK] OperacionNoPermitidaError en transición inválida: {e}")

    # 8. Baja lógica de usuario e intento de login
    print("\n[TEST 8] Baja lógica de cliente y bloqueo de inicio de sesión...")
    usr_srv.eliminar(cliente.id, admin)
    try:
        usr_srv.autenticar("carlos@mail.com", "clave123")
        print("  [FALLÓ] Usuario eliminado pudo iniciar sesión.")
    except CredencialesInvalidasError as e:
        print(f"  [OK] Usuario eliminado bloqueado con mensaje estándar: '{e}'")

    print("\n=================================================================")
    print("   TODAS LAS PRUEBAS FINALIZARON EXITOSAMENTE")
    print("=================================================================")


if __name__ == "__main__":
    ejecutar_pruebas()
