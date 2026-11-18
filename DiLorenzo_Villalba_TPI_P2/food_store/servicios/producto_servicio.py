from entidades.producto import Producto
from excepciones import EntidadNoEncontradaError
from servicios.categoria_servicio import CategoriaServicio


class ProductoServicio:
    """Servicio encargado de gestionar la colección y reglas de negocio de Producto."""

    def __init__(self, categoria_servicio: CategoriaServicio) -> None:
        self._productos: list[Producto] = []
        self._categoria_servicio: CategoriaServicio = categoria_servicio

    def listar(self) -> list[Producto]:
        return [p for p in self._productos if not p.eliminado]

    def listar_disponibles(self) -> list[Producto]:
        return [
            p
            for p in self._productos
            if not p.eliminado and p.disponible and p.stock > 0
        ]

    def listar_por_categoria(
        self, id_categoria: int, solo_disponibles: bool = False
    ) -> list[Producto]:
        categoria = self._categoria_servicio.obtener_por_id(id_categoria)
        productos = (
            self.listar_disponibles() if solo_disponibles else self.listar()
        )
        return [p for p in productos if p.categoria == categoria]

    def obtener_por_id(self, id_producto: int) -> Producto:
        for producto in self._productos:
            if producto.id == id_producto and not producto.eliminado:
                return producto
        raise EntidadNoEncontradaError(
            f"No se encontró un producto activo con id {id_producto}."
        )

    def crear(
        self,
        nombre: str,
        descripcion: str,
        precio: float,
        stock: int,
        imagen: str,
        disponible: bool,
        id_categoria: int,
    ) -> Producto:
        categoria = self._categoria_servicio.obtener_por_id(id_categoria)
        nuevo = Producto(
            nombre=nombre,
            precio=precio,
            descripcion=descripcion,
            stock=stock,
            imagen=imagen,
            disponible=disponible,
            categoria=categoria,
        )
        self._productos.append(nuevo)
        return nuevo

    def editar(
        self,
        id_producto: int,
        nombre: str | None = None,
        descripcion: str | None = None,
        precio: float | None = None,
        stock: int | None = None,
        imagen: str | None = None,
        disponible: bool | None = None,
        id_categoria: int | None = None,
    ) -> Producto:
        producto = self.obtener_por_id(id_producto)
        nueva_categoria = None
        if id_categoria is not None:
            nueva_categoria = self._categoria_servicio.obtener_por_id(id_categoria)

        if nombre is not None and nombre.strip() != "":
            producto.nombre = nombre
        if descripcion is not None and descripcion.strip() != "":
            producto.descripcion = descripcion
        if precio is not None:
            producto.precio = precio
        if stock is not None:
            producto.stock = stock
        if imagen is not None and imagen.strip() != "":
            producto.imagen = imagen
        if disponible is not None:
            producto.disponible = disponible
        if nueva_categoria is not None:
            producto.categoria = nueva_categoria

        return producto

    def eliminar(self, id_producto: int) -> None:
        producto = self.obtener_por_id(id_producto)
        producto.eliminado = True
