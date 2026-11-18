from abc import ABC, abstractmethod


class Calculable(ABC):
    """Interfaz que define el comportamiento para calcular un total."""

    @abstractmethod
    def calcular_total(self) -> None:
        """Actualiza el total del objeto que la implementa."""
        pass
