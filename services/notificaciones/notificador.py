"""
================================================================================
SERVICIO DE NOTIFICACIONES
================================================================================
Generación de notificaciones para estudiantes sobre clases programadas.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

from datetime import datetime, timedelta
from typing import Dict

# Importar configuración
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from config import DB_PATH
except ImportError:
    DB_PATH = "database/abacom.db"


def calcular_hora_notificacion(hora_inicio: str) -> str:
    """
    Calcula la hora exacta de envío de notificación (30 minutos antes).

    Args:
        hora_inicio: Hora de inicio de la clase (HH:MM)

    Returns:
        str: Hora de notificación (HH:MM)
    """
    hora_obj = datetime.strptime(hora_inicio, "%H:%M")
    hora_notificacion = hora_obj - timedelta(minutes=30)
    return hora_notificacion.strftime("%H:%M")


def generar_notificacion_clase(
    id_curso: int,
    db_path: str = "database/abacom.db"
) -> Dict:
    """
    Genera una notificación para una clase (30 minutos antes).

    Args:
        id_curso: ID del curso

    Returns:
        dict: Datos de la notificación programada
    """
    from models.database import ejecutar_consulta

    # Obtener información del curso
    query = """
        SELECT c.nombre, c.horario_inicio, c.dias_semana,
               GROUP_CONCAT(e.celular) as celulares,
               GROUP_CONCAT(e.nombres_completos) as nombres
        FROM cursos c
        LEFT JOIN inscripciones i ON c.id_curso = i.id_curso
        LEFT JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
        WHERE c.id_curso = ? AND i.estado = 'inscrito'
        GROUP BY c.id_curso
    """

    curso = ejecutar_consulta(query, (id_curso,))
    if not curso:
        return {"exito": False, "error": "Curso no encontrado"}

    datos = curso[0]
    hora_notificacion = calcular_hora_notificacion(datos['horario_inicio'])

    mensaje = f"""
    📚 Recordatorio de Clase - ABACOM

    Curso: {datos['nombre']}
    Horario: {datos['horario_inicio']} - {datos['horario_fin']}

    La clase comienza en 30 minutos.
    """

    return {
        "exito": True,
        "id_curso": id_curso,
        "hora_notificacion": hora_notificacion,
        "mensaje": mensaje,
        "destinatarios": datos['celulares'].split(',') if datos['celulares'] else []
    }