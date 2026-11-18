from datetime import date
from calculable import Calculable
from entidades.base import Base
from entidades.detalle_pedido import DetallePedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones import (
    DatoInvalidoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    StockInsuficienteError,
)


class Pedido(Base, Calculable):
    """Entidad que representa un pedido realizado por un usuario."""

    def __init__(
        self,
        usuario: Usuario,
        forma_pago: FormaPago,
        fecha: date | None = None,
        estado: Estado = Estado.PENDIENTE,
    ) -> None:
        super().__init__()
        if not isinstance(usuario, Usuario) or usuario.eliminado:
            raise OperacionNoPermitidaError(
                "No se puede crear un pedido sin un usuario válido y activo."
            )
        self._usuario: Usuario = usuario
        self._fecha: date = fecha if fecha is not None else date.today()
        if not isinstance(estado, Estado):
            raise DatoInvalidoError("El estado inicial debe ser válido.")
        self._estado: Estado = estado
        self.forma_pago = forma_pago
        self._total: float = 0.0
        self._detalles: list[DetallePedido] = []
        self._usuario.agregar_pedido(self)

    @property
    def fecha(self) -> date:
        return self._fecha

    @property
    def estado(self) -> Estado:
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado: Estado) -> None:
        if not isinstance(nuevo_estado, Estado):
            raise DatoInvalidoError("El estado debe ser una instancia de Estado.")
        if nuevo_estado == self._estado:
            return
        transiciones_validas: dict[Estado, set[Estado]] = {
            Estado.PENDIENTE: {Estado.CONFIRMADO, Estado.CANCELADO},
            Estado.CONFIRMADO: {Estado.TERMINADO, Estado.CANCELADO},
            Estado.TERMINADO: set(),
            Estado.CANCELADO: set(),
        }
        if nuevo_estado not in transiciones_validas.get(self._estado, set()):
            raise OperacionNoPermitidaError(
                f"Transición de estado inválida: {self._estado.value} -> {nuevo_estado.value}."
            )
        self._estado = nuevo_estado

    @property
    def total(self) -> float:
        return self._total

    @property
    def forma_pago(self) -> FormaPago:
        return self._forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if not isinstance(valor, FormaPago):
            raise DatoInvalidoError("La forma de pago debe ser una instancia de FormaPago.")
        self._forma_pago: FormaPago = valor

    @property
    def usuario(self) -> Usuario:
        return self._usuario

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        return tuple(d for d in self._detalles if not d.eliminado)

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        if not isinstance(producto, Producto) or producto.eliminado:
            raise EntidadNoEncontradaError("El producto no existe o está eliminado.")
        if not producto.disponible:
            raise OperacionNoPermitidaError(
                f"El producto '{producto.nombre}' no se encuentra disponible."
            )
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise DatoInvalidoError("La cantidad del detalle debe ser mayor a 0.")

        detalle_existente = self.buscar_detalle_por_producto(producto)
        nueva_cantidad = cantidad + (
            detalle_existente.cantidad if detalle_existente is not None else 0
        )

        if nueva_cantidad > producto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente para '{producto.nombre}'. "
                f"Disponible: {producto.stock}, solicitado total: {nueva_cantidad}."
            )

        if detalle_existente is not None:
            detalle_existente.cantidad = nueva_cantidad
        else:
            nuevo_detalle = DetallePedido(cantidad=cantidad, producto=producto)
            self._detalles.append(nuevo_detalle)

        self.calcular_total()

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        for detalle in self._detalles:
            if not detalle.eliminado and detalle.producto == producto:
                return detalle
        return None

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is None:
            raise EntidadNoEncontradaError(
                "El producto indicado no forma parte de los detalles del pedido."
            )
        detalle.eliminado = True
        self._detalles.remove(detalle)
        self.calcular_total()

    def calcular_total(self) -> None:
        self._total = round(
            sum(d.subtotal for d in self._detalles if not d.eliminado), 2
        )

    def __str__(self) -> str:
        return (
            f"[{self.id}] Fecha: {self.fecha} | Usuario: {self.usuario.nombre} {self.usuario.apellido} | "
            f"Estado: {self.estado.value} | Pago: {self.forma_pago.value} | Total: ${self.total:.2f}"
        )
