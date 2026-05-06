"""Input validation helpers for console application."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.servicios import validar_cedula_ecuador


def validar_cedula_input(cedula: str) -> bool:
    """Validate Ecuadorian ID format"""
    return validar_cedula_ecuador(cedula)


def validar_numero_input(valor: str) -> bool:
    """Check if input can be converted to integer"""
    try:
        int(valor)
        return True
    except ValueError:
        return False


def validar_sino_input(respuesta: str) -> bool:
    """Check if input is s or n"""
    return respuesta.lower() in ('s', 'n')


def solicitar_cedula(mensaje: str) -> str | None:
    """Request and validate cedula input"""
    cedula = input(mensaje).strip()
    if not validar_cedula_input(cedula):
        print("\n❌ Cédula inválida. Debe tener 10 dígitos.")
        return None
    return cedula


def solicitar_numero(mensaje: str) -> int | None:
    """Request and validate numeric input"""
    valor = input(mensaje).strip()
    if not validar_numero_input(valor):
        print("\n❌ Valor inválido")
        return None
    return int(valor)


def solicitar_texto(mensaje: str, requerido: bool = True) -> str | None:
    """Request text input"""
    texto = input(mensaje).strip()
    if requerido and not texto:
        print("\n❌ Este campo es requerido")
        return None
    return texto