from entidades.base import Base
from entidades.categoria import Categoria
from excepciones import DatoInvalidoError, PrecioInvalidoError


class Producto(Base):
    """Entidad que representa un producto comercializado en Food Store."""

    def __init__(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        stock: int,
        imagen: str,
        disponible: bool,
        categoria: Categoria,
    ) -> None:
        super().__init__()
        self._categoria: Categoria | None = None
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.imagen = imagen
        self.disponible = disponible
        self.categoria = categoria

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El nombre del producto no puede estar vacío.")
        self._nombre: str = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise PrecioInvalidoError("El precio debe ser un valor numérico.")
        if float(valor) < 0:
            raise PrecioInvalidoError("El precio no puede ser negativo.")
        self._precio: float = float(valor)

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("La descripción del producto no puede estar vacía.")
        self._descripcion: str = valor.strip()

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise DatoInvalidoError("El stock debe ser un número entero.")
        if valor < 0:
            raise DatoInvalidoError("El stock no puede ser negativo.")
        self._stock: int = valor

    @property
    def imagen(self) -> str:
        return self._imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("La imagen del producto no puede estar vacía.")
        self._imagen: str = valor.strip()

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatoInvalidoError("La disponibilidad debe ser un valor booleano.")
        self._disponible: bool = valor

    @property
    def categoria(self) -> Categoria:
        if self._categoria is None:
            raise DatoInvalidoError("El producto no tiene categoría asignada.")
        return self._categoria

    @categoria.setter
    def categoria(self, valor: Categoria) -> None:
        if not isinstance(valor, Categoria) or valor.eliminado:
            raise DatoInvalidoError("Debe asignar una categoría válida y activa.")
        if self._categoria is not None and self._categoria != valor:
            self._categoria.quitar_producto(self)
        self._categoria = valor
        valor.agregar_producto(self)

    def __str__(self) -> str:
        disp_str = "Disponible" if self.disponible else "No disponible"
        return (
            f"[{self.id}] {self.nombre} | ${self.precio:.2f} | "
            f"Stock: {self.stock} | Categoría: {self.categoria.nombre} | {disp_str}"
        )
