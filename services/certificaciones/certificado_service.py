"""
================================================================================
SERVICIO DE CERTIFICACIONES
================================================================================
Generación de certificados con aval del Ministerio del Trabajo.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

import uuid
from datetime import datetime
from typing import Dict

# Importar configuración
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from config import DB_PATH
except ImportError:
    DB_PATH = "database/abacom.db"


def generar_certificado(
    id_inscripcion: int,
    calificacion: float,
    db_path: str = DB_PATH
) -> Dict:
    """
    Genera un certificado con aval del Ministerio del Trabajo.

    Args:
        id_inscripcion: ID de la inscripción
        calificacion: Calificación obtenida (0-100)

    Returns:
        dict: Datos del certificado
    """
    from models.database import ejecutar_consulta, ejecutar_insert, ejecutar_modificacion
    from models.entities import Certificado, Inscripcion

    # Obtener datos de la inscripción
    query = """
        SELECT e.nombres_completos, e.identificacion,
               c.nombre as nombre_curso, c.fecha_inicio, c.fecha_fin,
               i.estado_certificacion
        FROM inscripciones i
        JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
        JOIN cursos c ON i.id_curso = c.id_curso
        WHERE i.id_inscripcion = ?
    """

    datos = ejecutar_consulta(query, (id_inscripcion,))
    if not datos:
        return {"exito": False, "error": "Inscripción no encontrada"}

    info = datos[0]

    # Determinar estado
    if calificacion < 70:
        estado = "REPROBADO"
        aval = None
    else:
        estado = "APROBADO"
        aval = "Ministerio del Trabajo - Ecuador"

    # Generar número de certificado único
    numero = f"ABACOM-{datetime.now().year}-{uuid.uuid4().hex[:8].upper()}"

    # Crear objeto Certificado
    certificado = Certificado(
        id_inscripcion=id_inscripcion,
        numero_certificado=numero,
        estado='emitido',
        aval_ministerio=aval
    )

    # Insertar certificado
    query_cert = """
        INSERT INTO certificaciones (
            id_inscripcion, numero_certificado, fecha_emision,
            estado, aval_ministerio
        ) VALUES (?, ?, DATE('now'), ?, ?)
    """

    try:
        id_cert = ejecutar_insert(
            query_cert,
            (id_inscripcion, numero, certificado.estado, aval)
        )

        # Actualizar inscripción
        cert_estado = 'aprobado' if calificacion >= 70 else 'reprobado'
        params = (cert_estado, calificacion,
                 "certificado" if calificacion >= 70 else "finalizado",
                 id_inscripcion)

        ejecutar_modificacion(
            """UPDATE inscripciones SET estado_certificacion = ?,
               calificacion = ?, estado = ? WHERE id_inscripcion = ?""",
            params
        )

        # Generar PDF usando el método del objeto
        pdf_path = certificado.generar_pdf()

        return {
            "exito": True,
            "id_certificacion": id_cert,
            "numero_certificado": numero,
            "estudiante": info['nombres_completos'],
            "curso": info['nombre_curso'],
            "calificacion": calificacion,
            "estado": estado,
            "aval_ministerio": aval,
            "pdf_path": pdf_path,
            "mensaje": "Certificado generado exitosamente"
        }
    except Exception as e:
        return {"exito": False, "error": f"Error al generar certificado: {str(e)}"}