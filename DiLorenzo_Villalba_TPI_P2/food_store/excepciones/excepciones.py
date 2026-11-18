class FoodStoreError(Exception):
    """Excepción base para todas las reglas de negocio de Food Store."""
    pass


class EntidadNoEncontradaError(FoodStoreError):
    """Se lanza cuando un id no existe o la entidad está eliminada."""
    pass


class DatoInvalidoError(FoodStoreError):
    """Se lanza cuando un dato es vacío o tiene un formato incorrecto."""
    pass


class PrecioInvalidoError(DatoInvalidoError):
    """Se lanza cuando el precio es negativo."""
    pass


class StockInsuficienteError(FoodStoreError):
    """Se lanza cuando la cantidad pedida supera el stock disponible o el stock es inválido."""
    pass


class DuplicadoError(FoodStoreError):
    """Se lanza cuando el mail de usuario o el nombre de categoría está repetido."""
    pass


class OperacionNoPermitidaError(FoodStoreError):
    """Se lanza en transiciones de estado inválidas, bajas no permitidas, etc."""
    pass


class CredencialesInvalidasError(FoodStoreError):
    """Se lanza cuando el mail o contraseña son incorrectos, o el usuario está eliminado."""
    pass
