from enum import Enum
from typing import TypeVar

T = TypeVar("T", bound=Enum)


def leer_texto(mensaje: str, permitir_vacio: bool = False) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor or permitir_vacio:
            return valor
        print("Error: El texto no puede estar vacío.")


def leer_entero(
    mensaje: str,
    minimo: int | None = None,
    permitir_vacio: bool = False,
) -> int | None:
    while True:
        texto = input(mensaje).strip()
        if permitir_vacio and texto == "":
            return None
        try:
            valor = int(texto)
            if minimo is not None and valor < minimo:
                print(f"Error: El número debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")


def leer_flotante(
    mensaje: str,
    minimo: float | None = None,
    permitir_vacio: bool = False,
) -> float | None:
    while True:
        texto = input(mensaje).strip()
        if permitir_vacio and texto == "":
            return None
        try:
            valor = float(texto)
            if minimo is not None and valor < minimo:
                print(f"Error: El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Error: Debe ingresar un número válido.")


def leer_confirmacion(mensaje: str, permitir_vacio: bool = False) -> bool | None:
    while True:
        texto = input(mensaje).strip().upper()
        if permitir_vacio and texto == "":
            return None
        if texto == "S":
            return True
        if texto == "N":
            return False
        print("Error: Ingrese 'S' para Sí o 'N' para No.")


def seleccionar_enum(
    tipo_enum: type[T],
    titulo: str,
    permitir_vacio: bool = False,
) -> T | None:
    opciones = list(tipo_enum)
    while True:
        print(f"\n{titulo}:")
        for idx, item in enumerate(opciones, start=1):
            print(f"{idx}. {item.value}")
        sufijo = " (Enter para conservar actual): " if permitir_vacio else ": "
        eleccion = input(f"Seleccione una opción (1-{len(opciones)}){sufijo}").strip()
        if permitir_vacio and eleccion == "":
            return None
        try:
            indice = int(eleccion)
            if 1 <= indice <= len(opciones):
                return opciones[indice - 1]
            print(f"Error: Seleccione un número entre 1 y {len(opciones)}.")
        except ValueError:
            print("Error: Debe ingresar un número válido.")
