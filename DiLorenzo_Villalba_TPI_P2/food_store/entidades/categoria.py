from __future__ import annotations
from typing import TYPE_CHECKING
from entidades.base import Base
from excepciones import DatoInvalidoError

if TYPE_CHECKING:
    from entidades.producto import Producto


class Categoria(Base):
    """Entidad que representa una categoría del catálogo de productos."""

    def __init__(self, nombre: str, descripcion: str) -> None:
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion
        self._productos: list[Producto] = []

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El nombre de la categoría no puede estar vacío.")
        self._nombre: str = valor.strip()

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("La descripción de la categoría no puede estar vacía.")
        self._descripcion: str = valor.strip()

    @property
    def productos(self) -> tuple[Producto, ...]:
        return tuple(self._productos)

    def agregar_producto(self, producto: Producto) -> None:
        if producto not in self._productos:
            self._productos.append(producto)

    def quitar_producto(self, producto: Producto) -> None:
        if producto in self._productos:
            self._productos.remove(producto)

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} - {self.descripcion}"
