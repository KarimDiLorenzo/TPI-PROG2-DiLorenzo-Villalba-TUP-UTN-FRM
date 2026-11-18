from entidades.base import Base
from entidades.producto import Producto
from excepciones import DatoInvalidoError


class DetallePedido(Base):
    """Entidad que representa una línea de detalle dentro de un Pedido."""

    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        if not isinstance(producto, Producto):
            raise DatoInvalidoError("El detalle debe tener un producto válido.")
        self._producto: Producto = producto
        self._precio_unitario: float = producto.precio
        self._subtotal: float = 0.0
        self.cantidad = cantidad

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise DatoInvalidoError("La cantidad del detalle debe ser un entero mayor a 0.")
        self._cantidad: int = valor
        self._subtotal = round(self._cantidad * self._precio_unitario, 2)

    @property
    def subtotal(self) -> float:
        return self._subtotal

    @property
    def producto(self) -> Producto:
        return self._producto

    def __str__(self) -> str:
        return (
            f"{self.producto.nombre} x {self.cantidad} "
            f"(${self._precio_unitario:.2f} c/u) = ${self.subtotal:.2f}"
        )
