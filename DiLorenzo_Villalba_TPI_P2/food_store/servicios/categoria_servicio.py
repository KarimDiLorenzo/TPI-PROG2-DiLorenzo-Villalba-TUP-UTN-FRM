from entidades.categoria import Categoria
from excepciones import (
    DuplicadoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
)


class CategoriaServicio:
    """Servicio encargado de gestionar la colección y reglas de negocio de Categoría."""

    def __init__(self) -> None:
        self._categorias: list[Categoria] = []

    def listar(self) -> list[Categoria]:
        return [c for c in self._categorias if not c.eliminado]

    def obtener_por_id(self, id_categoria: int) -> Categoria:
        for categoria in self._categorias:
            if categoria.id == id_categoria and not categoria.eliminado:
                return categoria
        raise EntidadNoEncontradaError(
            f"No se encontró una categoría activa con id {id_categoria}."
        )

    def _validar_nombre_unico(self, nombre: str, id_excluir: int | None = None) -> None:
        nombre_norm = nombre.strip().lower()
        for categoria in self._categorias:
            if not categoria.eliminado and categoria.id != id_excluir:
                if categoria.nombre.lower() == nombre_norm:
                    raise DuplicadoError(
                        f"Ya existe una categoría con el nombre '{nombre.strip()}'."
                    )

    def crear(self, nombre: str, descripcion: str) -> Categoria:
        self._validar_nombre_unico(nombre)
        nueva = Categoria(nombre=nombre, descripcion=descripcion)
        self._categorias.append(nueva)
        return nueva

    def editar(
        self,
        id_categoria: int,
        nombre: str | None = None,
        descripcion: str | None = None,
    ) -> Categoria:
        categoria = self.obtener_por_id(id_categoria)
        if nombre is not None and nombre.strip() != "":
            self._validar_nombre_unico(nombre, id_excluir=categoria.id)
            categoria.nombre = nombre
        if descripcion is not None and descripcion.strip() != "":
            categoria.descripcion = descripcion
        return categoria

    def eliminar(self, id_categoria: int) -> None:
        categoria = self.obtener_por_id(id_categoria)
        productos_activos = [p for p in categoria.productos if not p.eliminado]
        if len(productos_activos) > 0:
            raise OperacionNoPermitidaError(
                f"No se puede eliminar la categoría '{categoria.nombre}' porque tiene "
                f"{len(productos_activos)} producto(s) activo(s)."
            )
        categoria.eliminado = True
