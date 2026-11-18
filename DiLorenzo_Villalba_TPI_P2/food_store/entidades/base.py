from abc import ABC, abstractmethod
from datetime import datetime


class Base(ABC):
    """Superclase abstracta de todas las entidades del sistema."""

    _contador_id: int = 0

    @abstractmethod
    def __init__(self) -> None:
        Base._contador_id += 1
        self._id: int = Base._contador_id
        self._eliminado: bool = False
        self._creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self._id

    @property
    def eliminado(self) -> bool:
        return self._eliminado

    @eliminado.setter
    def eliminado(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise TypeError("El atributo eliminado debe ser booleano.")
        self._eliminado = valor

    @property
    def creado_en(self) -> datetime:
        return self._creado_en

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Base):
            return False
        return self._id == otro.id

    @abstractmethod
    def __str__(self) -> str:
        pass
