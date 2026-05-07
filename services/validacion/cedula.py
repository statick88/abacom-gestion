"""
================================================================================
VALIDACIÓN DE CÉDULA ECUATORIANA
================================================================================
Módulo de validación de cédula de identidad para Ecuador.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

from typing import Tuple


def validar_cedula_ecuador(cedula: str) -> bool:
    """
    Valida que la cédula tenga formato válido para Ecuador.

    Validaciones realizadas:
    - Longitud exacta: 10 dígitos
    - Primeros 2 dígitos deben estar entre 01-24 (código de provincia)
    - Solo contiene dígitos numéricos

    Args:
        cedula: Número de cédula de identidad (puede incluir espacios o guiones).

    Returns:
        bool: True si la cédula es válida, False en caso contrario.

    Example:
        >>> validar_cedula_ecuador("1712345678")
        True
        >>> validar_cedula_ecuador("0012345678")
        False
    """
    # Validar que no esté vacía y sea string
    if not cedula or not isinstance(cedula, str):
        return False

    # Remover espacios y guiones
    cedula_limpia = cedula.replace(" ", "").replace("-", "")

    # Verificar que sean exactamente 10 dígitos
    if len(cedula_limpia) != 10 or not cedula_limpia.isdigit():
        return False

    # Validar código de provincia (01-24)
    try:
        provincia = int(cedula_limpia[:2])
        if provincia < 1 or provincia > 24:
            return False
    except ValueError:
        return False

    return True


def obtener_info_cedula(cedula: str) -> Tuple[bool, str]:
    """
    Valida la cédula y retorna información adicional.

    Args:
        cedula: Número de cédula de identidad.

    Returns:
        Tuple[bool, str]: (es_válida, mensaje explicativo).

    Example:
        >>> es_valida, mensaje = obtener_info_cedula("1712345678")
        >>> print(mensaje)
        Cédula válida
    """
    if not cedula or not isinstance(cedula, str):
        return False, "La cédula no puede estar vacía"

    cedula_limpia = cedula.replace(" ", "").replace("-", "")

    if len(cedula_limpia) != 10:
        return False, "La cédula debe tener exactamente 10 dígitos"

    if not cedula_limpia.isdigit():
        return False, "La cédula solo puede contener números"

    try:
        provincia = int(cedula_limpia[:2])
        if provincia < 1 or provincia > 24:
            return False, f"Código de provincia inválido: {provincia}"
    except ValueError:
        return False, "Error al procesar el código de provincia"

    return True, "Cédula válida"


def formatear_cedula(cedula: str) -> str:
    """
    Formatea una cédula removiendo espacios y guiones.

    Args:
        cedula: Número de cédula con formato opcional.

    Returns:
        str: Cédula formateada solo con dígitos.

    Example:
        >>> formatear_cedula("171-2345-678")
        '1712345678'
    """
    return cedula.replace(" ", "").replace("-", "") if cedula else ""