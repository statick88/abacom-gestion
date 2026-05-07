"""
================================================================================
SERVICIO DE INSCRIPCIONES
================================================================================
Gestión de inscripciones de estudiantes a cursos en ABACOM.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

from typing import Dict

# Importar configuración
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from config import DB_PATH
except ImportError:
    DB_PATH = "database/abacom.db"

# Importar función de validación de cédula
from services.validacion.cedula import validar_cedula_ecuador


def validar_inscripcion(
    cedula_estudiante: str,
    tiene_pdf_cedula: bool,
    tiene_pago: bool,
    estado_certificacion: str = "pendiente"
) -> Dict:
    """
    Valida que la inscripción cumpla todos los requisitos.

    Args:
        cedula_estudiante: Número de cédula
        tiene_pdf_cedula: Tiene copia PDF de cédula
        tiene_pago: Tiene comprobante de pago
        estado_certificacion: Estado de certificación

    Returns:
        dict: Con 'valida' y lista de errores
    """
    errores = []

    # Validar Cédula
    if not validar_cedula_ecuador(cedula_estudiante):
        errores.append("Cédula de identidad inválida")

    # Validar requisitos
    if not tiene_pdf_cedula:
        errores.append("Falta copia de cédula en PDF")

    if not tiene_pago:
        errores.append("Falta comprobante de pago")

    # Validar estado de certificación
    estados_validos = ["aprobado", "en_proceso", "pendiente"]
    if estado_certificacion.lower() not in estados_validos:
        errores.append("Estado de certificación inválido")

    return {
        "valida": len(errores) == 0,
        "errores": errores
    }


def inscribir_estudiante(
    id_estudiante: int,
    id_curso: int,
    tiene_pdf_cedula: bool = False,
    tiene_pago: bool = False,
    db_path: str = DB_PATH
) -> Dict:
    """
    Inscribe un estudiante en un curso.

    Args:
        id_estudiante: ID del estudiante
        id_curso: ID del curso
        tiene_pdf_cedula: Tiene PDF de cédula
        tiene_pago: Tiene pago

    Returns:
        dict: Resultado de la inscripción
    """
    from models.database import ejecutar_consulta, ejecutar_insert
    from models.entities import Inscripcion, Estudiante, Curso

    # Verificar estudiante existe
    estudiante_data = ejecutar_consulta(
        "SELECT identificacion FROM estudiantes WHERE id_estudiante = ?",
        (id_estudiante,)
    )
    if not estudiante_data:
        return {"exito": False, "error": "Estudiante no encontrado"}

    # Verificar curso existe
    curso_data = ejecutar_consulta(
        "SELECT capacidad, estado FROM cursos WHERE id_curso = ?",
        (id_curso,)
    )
    if not curso_data:
        return {"exito": False, "error": "Curso no encontrado"}

    if curso_data[0]['estado'] not in ['activo', 'en_curso']:
        return {"exito": False, "error": "El curso no está disponible para inscripciones"}

    # Verificar capacidad
    inscritos = ejecutar_consulta(
        "SELECT COUNT(*) as total FROM inscripciones WHERE id_curso = ? AND estado = 'inscrito'",
        (id_curso,)
    )
    if inscritos[0]['total'] >= curso_data[0]['capacidad']:
        return {"exito": False, "error": "El curso ha alcanzado su capacidad máxima"}

    # Verificar no esté ya inscrito
    ya_inscrito = ejecutar_consulta(
        """SELECT id_inscripcion FROM inscripciones
           WHERE id_estudiante = ? AND id_curso = ? AND estado = 'inscrito'""",
        (id_estudiante, id_curso)
    )
    if ya_inscrito:
        return {"exito": False, "error": "El estudiante ya está inscrito en este curso"}

    # Crear objeto Inscripcion y validar requisitos
    inscripcion = Inscripcion(
        id_estudiante=id_estudiante,
        id_curso=id_curso,
        tiene_pdf_cedula=tiene_pdf_cedula,
        tiene_pago=tiene_pago
    )

    validacion = inscripcion.validar_requisitos()
    if not validacion["valida"]:
        return {
            "exito": False,
            "error": "Requisitos incompletos",
            "detalles": validacion["errores"]
        }

    # Registrar inscripción
    query = """
        INSERT INTO inscripciones (
            id_estudiante, id_curso, tiene_pdf_cedula, tiene_pago, estado
        ) VALUES (?, ?, ?, ?, 'inscrito')
    """

try:
        id_inscripcion = ejecutar_insert(
            query,
            (id_estudiante, id_curso, tiene_pdf_cedula, tiene_pago)
        )

        return {
            "exito": True,
            "id_inscripcion": id_inscripcion,
            "mensaje": "Inscripción realizada exitosamente"
        }
    except Exception as e:
        return {"exito": False, "error": f"Error al inscribir: {str(e)}"}