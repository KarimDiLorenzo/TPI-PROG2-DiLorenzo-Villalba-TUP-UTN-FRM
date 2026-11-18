from entidades.pedido import Pedido
from entidades.usuario import Usuario
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones import (
    DatoInvalidoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
)
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


class PedidoServicio:
    """Servicio encargado de gestionar los pedidos, detalles y control de stock."""

    def __init__(
        self,
        usuario_servicio: UsuarioServicio,
        producto_servicio: ProductoServicio,
    ) -> None:
        self._pedidos: list[Pedido] = []
        self._usuario_servicio: UsuarioServicio = usuario_servicio
        self._producto_servicio: ProductoServicio = producto_servicio

    def listar(self) -> list[Pedido]:
        return [p for p in self._pedidos if not p.eliminado]

    def listar_por_usuario(self, usuario: Usuario) -> list[Pedido]:
        return [
            p for p in self._pedidos if not p.eliminado and p.usuario == usuario
        ]

    def obtener_por_id(self, id_pedido: int) -> Pedido:
        for pedido in self._pedidos:
            if pedido.id == id_pedido and not pedido.eliminado:
                return pedido
        raise EntidadNoEncontradaError(
            f"No se encontró un pedido activo con id {id_pedido}."
        )

    def obtener_por_id_y_usuario(self, id_pedido: int, usuario: Usuario) -> Pedido:
        pedido = self.obtener_por_id(id_pedido)
        if pedido.usuario != usuario:
            raise EntidadNoEncontradaError(
                f"No se encontró un pedido activo con id {id_pedido}."
            )
        return pedido

    def crear_pedido(
        self,
        id_usuario: int,
        forma_pago: FormaPago,
        items: list[tuple[int, int]],
    ) -> Pedido:
        """
        Crea un pedido con sus detalles.
        items es una lista de tuplas (id_producto, cantidad).
        Si ocurre algún error al agregar detalles, no se guarda el pedido ni se altera el stock.
        """
        if not items:
            raise DatoInvalidoError("El pedido debe contener al menos un detalle.")

        usuario = self._usuario_servicio.obtener_por_id(id_usuario)
        pedido = Pedido(usuario=usuario, forma_pago=forma_pago)

        for id_producto, cantidad in items:
            producto = self._producto_servicio.obtener_por_id(id_producto)
            pedido.agregar_detalle(cantidad=cantidad, producto=producto)

        pedido.calcular_total()

        for detalle in pedido.detalles:
            detalle.producto.stock -= detalle.cantidad

        self._pedidos.append(pedido)
        return pedido

    def actualizar_pedido(
        self,
        id_pedido: int,
        nuevo_estado: Estado | None = None,
        nueva_forma_pago: FormaPago | None = None,
    ) -> Pedido:
        pedido = self.obtener_por_id(id_pedido)
        estado_anterior = pedido.estado

        if nuevo_estado is not None and nuevo_estado != estado_anterior:
            pedido.estado = nuevo_estado
            if nuevo_estado == Estado.CANCELADO:
                self._devolver_stock(pedido)

        if nueva_forma_pago is not None:
            if pedido.estado in (Estado.TERMINADO, Estado.CANCELADO) and nuevo_estado is None:
                raise OperacionNoPermitidaError(
                    f"No se puede modificar un pedido en estado {pedido.estado.value}."
                )
            pedido.forma_pago = nueva_forma_pago

        return pedido

    def eliminar(self, id_pedido: int) -> None:
        pedido = self.obtener_por_id(id_pedido)
        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            self._devolver_stock(pedido)

        for detalle in pedido.detalles:
            detalle.eliminado = True
        pedido.eliminado = True

    def _devolver_stock(self, pedido: Pedido) -> None:
        for detalle in pedido.detalles:
            detalle.producto.stock += detalle.cantidad
