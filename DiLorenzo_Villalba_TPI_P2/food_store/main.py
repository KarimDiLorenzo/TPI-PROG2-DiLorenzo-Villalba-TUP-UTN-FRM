from consola import crear_menu
from entidades.usuario import Usuario
from enums.forma_pago import FormaPago
from enums.rol import Rol
from excepciones import CredencialesInvalidasError
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


def cargar_datos_iniciales(
    categoria_servicio: CategoriaServicio,
    producto_servicio: ProductoServicio,
    usuario_servicio: UsuarioServicio,
    pedido_servicio: PedidoServicio,
) -> None:
    """Carga el administrador inicial y datos de prueba en memoria."""
    usuario_servicio.crear(
        nombre="Ana",
        apellido="Pérez",
        mail="admin@foodstore.com",
        celular="2615000001",
        contrasenia="admin123",
        rol=Rol.ADMIN,
    )
    cliente = usuario_servicio.crear(
        nombre="Juan",
        apellido="Gómez",
        mail="juan@cliente.com",
        celular="2615000002",
        contrasenia="cliente123",
        rol=Rol.USUARIO,
    )

    cat_hamburguesas = categoria_servicio.crear(
        nombre="Hamburguesas",
        descripcion="Hamburguesas caseras gourmet con papas",
    )
    cat_pizzas = categoria_servicio.crear(
        nombre="Pizzas",
        descripcion="Pizzas a la piedra de masa madre",
    )
    cat_bebidas = categoria_servicio.crear(
        nombre="Bebidas",
        descripcion="Gaseosas, aguas saborizadas y cervezas artesanales",
    )

    prod_doble = producto_servicio.crear(
        nombre="Hamburguesa Doble Cheddar",
        descripcion="Doble medallón de carne 180g, cheddar, panceta y papas",
        precio=8500.0,
        stock=20,
        imagen="doble_cheddar.jpg",
        disponible=True,
        id_categoria=cat_hamburguesas.id,
    )
    producto_servicio.crear(
        nombre="Pizza Muzzarella",
        descripcion="Salsa de tomate natural, muzzarella, aceitunas y orégano",
        precio=9200.0,
        stock=15,
        imagen="pizza_muzza.jpg",
        disponible=True,
        id_categoria=cat_pizzas.id,
    )
    prod_gaseosa = producto_servicio.crear(
        nombre="Gaseosa Cola 500ml",
        descripcion="Botella individual 500ml fría",
        precio=2100.0,
        stock=50,
        imagen="cola_500.jpg",
        disponible=True,
        id_categoria=cat_bebidas.id,
    )

    pedido_servicio.crear_pedido(
        id_usuario=cliente.id,
        forma_pago=FormaPago.TARJETA,
        items=[(prod_doble.id, 2), (prod_gaseosa.id, 2)],
    )


def iniciar_sesion(usuario_servicio: UsuarioServicio) -> Usuario | None:
    """Gestiona hasta 3 intentos de inicio de sesión."""
    intentos_maximos: int = 3
    for intento in range(1, intentos_maximos + 1):
        print("\n=== FOOD STORE - INICIO DE SESIÓN ===")
        mail = input("Mail: ").strip()
        contrasenia = input("Contraseña: ").strip()
        try:
            usuario = usuario_servicio.autenticar(mail=mail, contrasenia=contrasenia)
            print(
                f"\nBienvenido/a, {usuario.nombre} {usuario.apellido} [{usuario.rol.value}]"
            )
            return usuario
        except CredencialesInvalidasError as e:
            restantes = intentos_maximos - intento
            if restantes > 0:
                print(f"{e}. Intentos restantes: {restantes}.")
            else:
                print(f"{e}. Se agotaron los 3 intentos. El programa terminará.")
    return None


def main() -> None:
    categoria_servicio = CategoriaServicio()
    producto_servicio = ProductoServicio(categoria_servicio=categoria_servicio)
    usuario_servicio = UsuarioServicio()
    pedido_servicio = PedidoServicio(
        usuario_servicio=usuario_servicio,
        producto_servicio=producto_servicio,
    )

    cargar_datos_iniciales(
        categoria_servicio=categoria_servicio,
        producto_servicio=producto_servicio,
        usuario_servicio=usuario_servicio,
        pedido_servicio=pedido_servicio,
    )

    while True:
        usuario_sesion = iniciar_sesion(usuario_servicio)
        if usuario_sesion is None:
            break

        menu = crear_menu(
            usuario=usuario_sesion,
            categoria_servicio=categoria_servicio,
            producto_servicio=producto_servicio,
            usuario_servicio=usuario_servicio,
            pedido_servicio=pedido_servicio,
        )
        cerrar_sesion = menu.mostrar()
        if not cerrar_sesion:
            break


if __name__ == "__main__":
    main()
