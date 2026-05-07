# Inscripciones service module
from services.inscripciones.inscripcion_service import (
    inscribir_estudiante,
    validar_inscripcion
)

__all__ = [
    'inscribir_estudiante',
    'validar_inscripcion'
]