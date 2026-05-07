# Estudiantes service module
from services.estudiantes.estudiante_service import (
    registrar_estudiante,
    obtener_estudiante_por_cedula,
    listar_estudiantes
)

__all__ = [
    'registrar_estudiante',
    'obtener_estudiante_por_cedula',
    'listar_estudiantes'
]