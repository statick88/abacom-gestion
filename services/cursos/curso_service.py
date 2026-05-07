"""
================================================================================
SERVICIO DE CURSOS
================================================================================
Gestión de cursos del sistema de gestión educativa ABACOM.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

from datetime import datetime
from typing import Optional, List, Dict

# Importar configuración
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from config import DB_PATH
except ImportError:
    DB_PATH = "database/abacom.db"


def validar_periodo_academico(fecha_inicio: str, periodo: int) -> bool:
    """
    Valida que la fecha de inicio corresponda al período académico.

    Args:
        fecha_inicio: Fecha de inicio del curso (formato YYYY-MM-DD)
        periodo: Período académico (ej. 2026)

    Returns:
        bool: True si corresponde al período
    """
    fecha = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    return fecha.year == periodo


def calcular_duracion_semanas(fecha_inicio: str, fecha_fin: str) -> int:
    """Calcula la duración en semanas del curso."""
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    return (fin - inicio).days // 7


def registrar_curso(
    codigo: str,
    nombre: str,
    modalidad: str,
    fecha_inicio: str,
    fecha_fin: str,
    horario_inicio: str,
    horario_fin: str,
    dias_semana: str,
    inversion: float,
    id_docente: int = None,
    capacidad: int = 30,
    db_path: str = DB_PATH
) -> Dict:
    """
    Registra un nuevo curso en el sistema.

    Args:
        codigo: Código del curso (ej. 01, 02)
        nombre: Nombre del curso
        modalidad: Online/Virtual/Presencial
        fecha_inicio: Fecha de inicio (YYYY-MM-DD)
        fecha_fin: Fecha de fin (YYYY-MM-DD)
        horario_inicio: Hora de inicio (HH:MM)
        horario_fin: Hora de fin (HH:MM)
        dias_semana: Días de clase (ej. "Lunes,Miércoles,Viernes")
        inversion: Costo del curso
        id_docente: ID del docente asignado
        capacidad: Capacidad máxima de estudiantes

    Returns:
        dict: Resultado con 'exito' y datos del curso o 'error'
    """
    from models.database import ejecutar_consulta, ejecutar_insert
    from models.entities import Curso

    # Crear objeto Curso
    curso = Curso(
        codigo=codigo,
        nombre=nombre,
        modalidad=modalidad,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        horario_inicio=horario_inicio,
        horario_fin=horario_fin,
        dias_semana=dias_semana,
        inversion=inversion,
        id_docente=id_docente,
        capacidad=capacidad
    )

    # Validar período académico usando el método del objeto
    if not validar_periodo_academico(fecha_inicio, 2026):
        return {
            "exito": False,
            "error": f"El curso debe iniciar en el período académico 2026."
        }

    # Verificar código único
    existente = ejecutar_consulta(
        "SELECT id_curso FROM cursos WHERE codigo = ?",
        (codigo,)
    )
    if existente:
        return {
            "exito": False,
            "error": f"Ya existe un curso con el código {codigo}."
        }

    # Insertar curso
    query = """
        INSERT INTO cursos (
            codigo, nombre, modalidad, fecha_inicio, fecha_fin,
            horario_inicio, horario_fin, dias_semana, inversion,
            id_docente, capacidad, periodo_academico
        ) VALUES (?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, 2026)
    """

    try:
        id_curso = ejecutar_insert(
            query,
            (codigo, nombre, modalidad, fecha_inicio, fecha_fin,
             horario_inicio, horario_fin, dias_semana, inversion,
             id_docente, capacidad)
        )

        return {
            "exito": True,
            "id_curso": id_curso,
            "duracion_semanas": curso.calcular_duracion_semanas(),
            "mensaje": "Curso registrado exitosamente."
        }
    except Exception as e:
        return {
            "exito": False,
            "error": f"Error al registrar curso: {str(e)}"
        }


def listar_cursos(estado: str = None, db_path: str = DB_PATH) -> List[Dict]:
    """Lista cursos según estado."""
    from models.database import ejecutar_consulta

    if estado:
        return ejecutar_consulta(
            "SELECT * FROM cursos WHERE estado = ? ORDER BY fecha_inicio",
            (estado,)
        )
    return ejecutar_consulta(
        "SELECT * FROM cursos ORDER BY fecha_inicio"
    )