from __future__ import annotations
from typing import TYPE_CHECKING
from entidades.base import Base
from enums.rol import Rol
from excepciones import DatoInvalidoError

if TYPE_CHECKING:
    from entidades.pedido import Pedido


class Usuario(Base):
    """Entidad que representa a un usuario del sistema (ADMIN o USUARIO)."""

    def __init__(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.cambiar_contrasenia(contrasenia)
        self.rol = rol
        self._pedidos: list[Pedido] = []

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El nombre del usuario no puede estar vacío.")
        self._nombre: str = valor.strip()

    @property
    def apellido(self) -> str:
        return self._apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El apellido del usuario no puede estar vacío.")
        self._apellido: str = valor.strip()

    @property
    def mail(self) -> str:
        return self._mail

    @mail.setter
    def mail(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El mail no puede estar vacío.")
        limpio = valor.strip()
        if "@" not in limpio or "." not in limpio:
            raise DatoInvalidoError("El mail debe tener un formato válido (contener '@' y '.').")
        self._mail: str = limpio

    @property
    def celular(self) -> str:
        return self._celular

    @celular.setter
    def celular(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El celular no puede estar vacío.")
        self._celular: str = valor.strip()

    def cambiar_contrasenia(self, nueva_contrasenia: str) -> None:
        if not isinstance(nueva_contrasenia, str) or not nueva_contrasenia.strip():
            raise DatoInvalidoError("La contraseña no puede estar vacía.")
        self._contrasenia: str = nueva_contrasenia.strip()

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        return self._contrasenia == contrasenia

    @property
    def rol(self) -> Rol:
        return self._rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        if not isinstance(valor, Rol):
            raise DatoInvalidoError("El rol debe ser una instancia válida de Rol.")
        self._rol: Rol = valor

    @property
    def pedidos(self) -> tuple[Pedido, ...]:
        return tuple(self._pedidos)

    def agregar_pedido(self, pedido: Pedido) -> None:
        if pedido not in self._pedidos:
            self._pedidos.append(pedido)

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.nombre} {self.apellido} | "
            f"Mail: {self.mail} | Cel: {self.celular} | Rol: {self.rol.value}"
        )
