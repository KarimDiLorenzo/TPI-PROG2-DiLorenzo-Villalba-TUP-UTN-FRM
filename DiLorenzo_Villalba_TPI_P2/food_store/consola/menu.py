from abc import ABC, abstractmethod
from entidades.usuario import Usuario


class Menu(ABC):
    """Clase abstracta para representar el menú según el rol del usuario."""

    def __init__(self, usuario: Usuario) -> None:
        self._usuario: Usuario = usuario

    @abstractmethod
    def mostrar(self) -> bool:
        """
        Ejecuta el ciclo del menú.
        Retorna True para cerrar sesión o False para salir del programa.
        """
        pass
