from entidades.usuario import Usuario
from enums.rol import Rol
from consola.menu import Menu
from consola.menu_administrador import MenuAdministrador
from consola.menu_cliente import MenuCliente
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio


def crear_menu(
    usuario: Usuario,
    categoria_servicio: CategoriaServicio,
    producto_servicio: ProductoServicio,
    usuario_servicio: UsuarioServicio,
    pedido_servicio: PedidoServicio,
) -> Menu:
    """Fábrica polimórfica que retorna el menú correspondiente al rol del usuario."""
    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(
            usuario=usuario,
            categoria_servicio=categoria_servicio,
            producto_servicio=producto_servicio,
            usuario_servicio=usuario_servicio,
            pedido_servicio=pedido_servicio,
        )
    return MenuCliente(
        usuario=usuario,
        categoria_servicio=categoria_servicio,
        producto_servicio=producto_servicio,
        pedido_servicio=pedido_servicio,
    )


__all__ = [
    "Menu",
    "MenuAdministrador",
    "MenuCliente",
    "crear_menu",
]
