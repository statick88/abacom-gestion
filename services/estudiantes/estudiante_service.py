"""
================================================================================
SERVICIO DE ESTUDIANTES
================================================================================
Gestión de estudiantes del sistema de gestión educativa ABACOM.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

from typing import Optional, List, Dict, Any
import sys
from pathlib import Path

# Configurar path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from config import DB_PATH
except ImportError:
    DB_PATH = "database/abacom.db"

from models.database import (
    ejecutar_consulta,
    ejecutar_insert,
    DatabaseError,
)
from models.entities import Estudiante
from services.validacion.cedula import validar_cedula_ecuador


def registrar_estudiante(
    identificacion: str,
    nombres_completos: str,
    celular: str,
    correo_electronico: str,
    telefono_fijo: Optional[str] = None,
    direccion: Optional[str] = None,
    fecha_nacimiento: Optional[str] = None,
    db_path: str = DB_PATH,
) -> Dict[str, Any]:
    """
    Registra un nuevo estudiante en el sistema.

    Args:
        identificacion: Cédula de identidad (10 dígitos Ecuador).
        nombres_completos: Nombres completos del estudiante.
        celular: Número de celular.
        correo_electronico: Correo electrónico.
        telefono_fijo: Teléfono fijo (opcional).
        direccion: Dirección de domicilio (opcional).
        fecha_nacimiento: Fecha de nacimiento (opcional).
        db_path: Ruta a la base de datos.

    Returns:
        Dict con 'exito' (bool) y:
        - Si éxito: 'id_estudiante', 'mensaje'
        - Si error: 'error'

    Raises:
        DatabaseError: Si ocurre un error de base de datos.
    """
    # Crear objeto Estudiante para validación
    estudiante = Estudiante(
        identificacion=identificacion,
        nombres_completos=nombres_completos,
        celular=celular,
        correo_electronico=correo_electronico,
        telefono_fijo=telefono_fijo,
        direccion=direccion,
        fecha_nacimiento=fecha_nacimiento,
    )

    # Validar cédula
    if not estudiante.validar_cedula():
        return {
            "exito": False,
            "error": "Cédula de identidad inválida. Debe tener 10 dígitos.",
        }

    # Verificar que no exista otro estudiante con la misma cédula
    try:
        existente = ejecutar_consulta(
            "SELECT id_estudiante FROM estudiantes WHERE identificacion = ?",
            (identificacion,),
            db_path=db_path,
        )
        if existente:
            return {
                "exito": False,
                "error": "Ya existe un estudiante registrado con esta cédula.",
            }
    except DatabaseError as e:
        return {
            "exito": False,
            "error": f"Error al verificar estudiante: {e.message}",
        }

    # Insertar estudiante
    query = """
        INSERT INTO estudiantes (
            identificacion, nombres_completos, telefono_fijo,
            celular, correo_electronico, direccion, fecha_nacimiento
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    try:
        id_estudiante = ejecutar_insert(
            query,
            (
                identificacion,
                nombres_completos,
                telefono_fijo,
                celular,
                correo_electronico,
                direccion,
                fecha_nacimiento,
            ),
            db_path=db_path,
        )

        return {
            "exito": True,
            "id_estudiante": id_estudiante,
            "mensaje": "Estudiante registrado exitosamente.",
        }

    except DatabaseError as e:
        return {
            "exito": False,
            "error": f"Error al registrar estudiante: {e.message}",
        }


def obtener_estudiante_por_cedula(
    cedula: str, db_path: str = DB_PATH
) -> Optional[Dict[str, Any]]:
    """
    Obtiene un estudiante por su número de cédula.

    Args:
        cedula: Número de cédula de identidad.
        db_path: Ruta a la base de datos.

    Returns:
        Dict con los datos del estudiante, o None si no existe.

    Raises:
        DatabaseError: Si ocurre un error de base de datos.
    """
    try:
        resultados = ejecutar_consulta(
            "SELECT * FROM estudiantes WHERE identificacion = ?",
            (cedula,),
            db_path=db_path,
        )
        return resultados[0] if resultados else None

    except DatabaseError:
        return None


def listar_estudiantes(db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """
    Lista todos los estudiantes con estado activo.

    Args:
        db_path: Ruta a la base de datos.

    Returns:
        List[Dict]: Lista de estudiantes ordenados por nombre.

    Raises:
        DatabaseError: Si ocurre un error de base de datos.
    """
    try:
        return ejecutar_consulta(
            "SELECT * FROM estudiantes WHERE estado = 'activo' "
            "ORDER BY nombres_completos",
            db_path=db_path,
        )
    except DatabaseError:
        return []


def actualizar_estudiante(
    id_estudiante: int,
    nombres_completos: Optional[str] = None,
    celular: Optional[str] = None,
    correo_electronico: Optional[str] = None,
    telefono_fijo: Optional[str] = None,
    direccion: Optional[str] = None,
    estado: Optional[str] = None,
    db_path: str = DB_PATH,
) -> Dict[str, Any]:
    """
    Actualiza los datos de un estudiante existente.

    Args:
        id_estudiante: ID del estudiante a actualizar.
        nombres_completos: Nuevo nombre (opcional).
        celular: Nuevo celular (opcional).
        correo_electronico: Nuevo correo (opcional).
        telefono_fijo: Nuevo teléfono fijo (opcional).
        direccion: Nueva dirección (opcional).
        estado: Nuevo estado (opcional).
        db_path: Ruta a la base de datos.

    Returns:
        Dict con 'exito' (bool) y 'mensaje' o 'error'.

    Raises:
        DatabaseError: Si ocurre un error de base de datos.
    """
    # Construir consulta dinámicamente solo con campos no nulos
    campos: List[str] = []
    valores: List[Any] = []

    if nombres_completos is not None:
        campos.append("nombres_completos = ?")
        valores.append(nombres_completos)

    if celular is not None:
        campos.append("celular = ?")
        valores.append(celular)

    if correo_electronico is not None:
        campos.append("correo_electronico = ?")
        valores.append(correo_electronico)

    if telefono_fijo is not None:
        campos.append("telefono_fijo = ?")
        valores.append(telefono_fijo)

    if direccion is not None:
        campos.append("direccion = ?")
        valores.append(direccion)

    if estado is not None:
        campos.append("estado = ?")
        valores.append(estado)

    if not campos:
        return {
            "exito": False,
            "error": "No hay campos para actualizar.",
        }

    # Agregar ID al final
    valores.append(id_estudiante)

    query = f"UPDATE estudiantes SET {', '.join(campos)} WHERE id_estudiante = ?"

    try:
        filas_afectadas = ejecutar_modificacion(
            query, tuple(valores), db_path=db_path
        )

        if filas_afectadas > 0:
            return {
                "exito": True,
                "mensaje": "Estudiante actualizado exitosamente.",
            }
        return {
            "exito": False,
            "error": "Estudiante no encontrado.",
        }

    except DatabaseError as e:
        return {
            "exito": False,
            "error": f"Error al actualizar estudiante: {e.message}",
        }


def eliminar_estudiante(
    id_estudiante: int, db_path: str = DB_PATH
) -> Dict[str, Any]:
    """
    Elimina (desactiva) un estudiante del sistema.

    Args:
        id_estudiante: ID del estudiante a eliminar.
        db_path: Ruta a la base de datos.

    Returns:
        Dict con 'exito' (bool) y 'mensaje' o 'error'.

    Raises:
        DatabaseError: Si ocurre un error de base de datos.
    """
    return actualizar_estudiante(
        id_estudiante=id_estudiante,
        estado="inactivo",
        db_path=db_path,
    )