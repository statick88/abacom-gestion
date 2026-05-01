"""
================================================================================
SERVICIOS DEL SISTEMA DE GESTIÓN EDUCATIVA ABACOM
================================================================================
Implementación de reglas de negocio usando programación funcional
que evolucionará a orientación a objetos.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from decimal import Decimal

# Importar configuración
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from config import DB_PATH
except ImportError:
    DB_PATH = "database/abacom.db"


# =============================================================================
# SERVICIO: VALIDACIONES
# =============================================================================

import re


def validar_correo_electronico(correo: str) -> bool:
    """
    Valida formato de correo electrónico.
    
    Args:
        correo: Dirección de correo electrónico
    
    Returns:
        bool: True si el formato es válido
    """
    if not correo or not isinstance(correo, str):
        return False
    
    # Patrón básico de correo electrónico
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, correo.strip()) is not None


def validar_telefono_ecuador(telefono: str) -> bool:
    """
    Valida formato de teléfono Ecuador (fijo o celular).
    
    Args:
        telefono: Número de teléfono
    
    Returns:
        bool: True si el formato es válido
    """
    if not telefono:
        return False
    
    # Limpiar número
    telefono_limpio = telefono.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    
    # Celular: 09X XXX XXXX (10 dígitos, empieza con 09)
    # Fijo: 02 XXX XXXX (9 dígitos, empieza con 0)
    if telefono_limpio.isdigit():
        if len(telefono_limpio) == 10 and telefono_limpio.startswith("09"):
            return True  # Celular
        if len(telefono_limpio) == 9 and telefono_limpio.startswith("0"):
            return True  # Fijo
    
    return False


# =============================================================================
# SERVICIO: ESTUDIANTES
# =============================================================================

def validar_cedula_ecuador(cedula: str) -> bool:
    """
    Valida que la cédula tenga formato válido para Ecuador.
    - Longitud exacta: 10 dígitos
    - Primeros 2 dígitos deben estar entre 01-24 (código provincia)
    
    Args:
        cedula: Número de cédula de identidad
    
    Returns:
        bool: True si es válida, False en caso contrario
    """
    if not cedula or not isinstance(cedula, str):
        return False

    # Remover espacios y guiones
    cedula_limpia = cedula.replace(" ", "").replace("-", "")

    # Verificar que sean exactamente 10 dígitos
    if len(cedula_limpia) != 10 or not cedula_limpia.isdigit():
        return False

    # Validar código de provincia (01-24)
    provincia = int(cedula_limpia[:2])
    if provincia < 1 or provincia > 24:
        return False

    return True


def registrar_estudiante(
    identificacion: str,
    nombres_completos: str,
    celular: str,
    correo_electronico: str,
    telefono_fijo: str = None,
    direccion: str = None,
    fecha_nacimiento: str = None,
    db_path: str = DB_PATH
) -> Dict:
    """
    Registra un nuevo estudiante en el sistema.
    
    Args:
        identificacion: Cédula de identidad (10 dígitos Ecuador)
        nombres_completos: Nombres completos del estudiante
        celular: Número de celular
        correo_electronico: Correo electrónico
        telefono_fijo: Teléfono fijo (opcional)
        direccion: Dirección (opcional)
        fecha_nacimiento: Fecha de nacimiento (opcional)
        db_path: Ruta a la base de datos
    
    Returns:
        dict: Resultado con 'exito' y datos del estudiante o 'error'
    """
    from models.database import ejecutar_modificacion, ejecutar_consulta
    from models.entities import Estudiante
    
    # Crear objeto Estudiante
    estudiante = Estudiante(
        identificacion=identificacion,
        nombres_completos=nombres_completos,
        celular=celular,
        correo_electronico=correo_electronico,
        telefono_fijo=telefono_fijo,
        direccion=direccion,
        fecha_nacimiento=fecha_nacimiento
    )
    
    # Validar cédula usando el método del objeto
    if not estudiante.validar_cedula():
        return {
            "exito": False,
            "error": "Cédula de identidad inválida. Debe tener 10 dígitos."
        }
    
    # Verificar que no exista
    existente = ejecutar_consulta(
        "SELECT id_estudiante FROM estudiantes WHERE identificacion = ?",
        (identificacion,)
    )
    if existente:
        return {
            "exito": False,
            "error": "Ya existe un estudiante registrado con esta cédula."
        }
    
    # Insertar estudiante
    query = """
        INSERT INTO estudiantes (
            identificacion, nombres_completos, telefono_fijo,
            celular, correo_electronico, direccion, fecha_nacimiento
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    
    try:
        id_estudiante = ejecutar_modificacion(
            query,
            (identificacion, nombres_completos, telefono_fijo,
             celular, correo_electronico, direccion, fecha_nacimiento)
        )
        
        return {
            "exito": True,
            "id_estudiante": id_estudiante,
            "mensaje": "Estudiante registrado exitosamente."
        }
    except Exception as e:
        return {
            "exito": False,
            "error": f"Error al registrar estudiante: {str(e)}"
        }


def obtener_estudiante_por_cedula(cedula: str, db_path: str = "database/abacom.db") -> Optional[Dict]:
    """Obtiene un estudiante por su número de cédula."""
    from models.database import ejecutar_consulta

    resultados = ejecutar_consulta(
        "SELECT * FROM estudiantes WHERE identificacion = ?",
        (cedula,)
    )
    return resultados[0] if resultados else None


def listar_estudiantes(db_path: str = "database/abacom.db") -> List[Dict]:
    """Lista todos los estudiantes activos."""
    from models.database import ejecutar_consulta
    return ejecutar_consulta(
        "SELECT * FROM estudiantes WHERE estado = 'activo' ORDER BY nombres_completos"
    )


# =============================================================================
# SERVICIO: CURSOS
# =============================================================================

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
    from models.database import ejecutar_modificacion, ejecutar_consulta
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
        id_curso = ejecutar_modificacion(
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
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 2026)
    """

    try:
        id_curso = ejecutar_modificacion(
            query,
            (codigo, nombre, modalidad, fecha_inicio, fecha_fin,
             horario_inicio, horario_fin, dias_semana, inversion,
             id_docente, capacidad)
        )

        return {
            "exito": True,
            "id_curso": id_curso,
            "duracion_semanas": calcular_duracion_semanas(fecha_inicio, fecha_fin),
            "mensaje": "Curso registrado exitosamente."
        }
    except Exception as e:
        return {
            "exito": False,
            "error": f"Error al registrar curso: {str(e)}"
        }


def listar_cursos(estado: str = None, db_path: str = "database/abadem.db") -> List[Dict]:
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


# =============================================================================
# SERVICIO: INSCRIPCIONES
# =============================================================================

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
    from models.database import ejecutar_consulta, ejecutar_modificacion
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
        id_inscripcion = ejecutar_modificacion(
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


# =============================================================================
# SERVICIO: NOTIFICACIONES
# =============================================================================

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


# =============================================================================
# SERVICIO: CERTIFICACIONES
# =============================================================================

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
    from models.database import ejecutar_consulta, ejecutar_modificacion
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
        id_cert = ejecutar_modificacion(
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


# =============================================================================
# SERVICIO: DOCENTES
# =============================================================================

def registrar_docente(
    nombres_completos: str,
    celular: str,
    correo_electronico: str,
    telefono: str = None,
    especializacion: str = None,
    db_path: str = DB_PATH
) -> Dict:
    """
    Registra un nuevo docente/facilitador en el sistema.
    """
    from models.database import ejecutar_modificacion, ejecutar_consulta
    
    # Verificar correo único
    existente = ejecutar_consulta(
        "SELECT id_docente FROM docentes WHERE correo_electronico = ?",
        (correo_electronico,)
    )
    if existente:
        return {
            "exito": False,
            "error": "Ya existe un docente registrado con este correo."
        }
    
    query = """
        INSERT INTO docentes (nombres_completos, telefono, celular, correo_electronico, especializacion)
        VALUES (?, ?, ?, ?, ?)
    """
    
    try:
        id_docente = ejecutar_modificacion(
            query,
            (nombres_completos, telefono, celular, correo_electronico, especializacion)
        )
        return {
            "exito": True,
            "id_docente": id_docente,
            "mensaje": "Docente registrado exitosamente."
        }
    except Exception as e:
        return {"exito": False, "error": f"Error al registrar docente: {str(e)}"}


def listar_docentes(estado: str = None, db_path: str = DB_PATH) -> List[Dict]:
    """Lista todos los docentes."""
    from models.database import ejecutar_consulta
    
    if estado:
        return ejecutar_consulta(
            "SELECT * FROM docentes WHERE estado = ? ORDER BY nombres_completos",
            (estado,)
        )
    return ejecutar_consulta(
        "SELECT * FROM docentes ORDER BY nombres_completos"
    )


def obtener_docente_por_id(id_docente: int, db_path: str = DB_PATH) -> Optional[Dict]:
    """Obtiene un docente por su ID."""
    from models.database import ejecutar_consulta
    
    resultados = ejecutar_consulta(
        "SELECT * FROM docentes WHERE id_docente = ?",
        (id_docente,)
    )
    return resultados[0] if resultados else None


def actualizar_docente(
    id_docente: int,
    nombres_completos: str = None,
    telefono: str = None,
    celular: str = None,
    correo_electronico: str = None,
    especializacion: str = None,
    estado: str = None,
    db_path: str = DB_PATH
) -> Dict:
    """Actualiza un docente."""
    from models.database import ejecutar_modificacion
    
    campos = []
    valores = []
    
    if nombres_completos:
        campos.append("nombres_completos = ?")
        valores.append(nombres_completos)
    if telefono is not None:
        campos.append("telefono = ?")
        valores.append(telefono)
    if celular:
        campos.append("celular = ?")
        valores.append(celular)
    if correo_electronico:
        campos.append("correo_electronico = ?")
        valores.append(correo_electronico)
    if especializacion is not None:
        campos.append("especializacion = ?")
        valores.append(especializacion)
    if estado:
        campos.append("estado = ?")
        valores.append(estado)
    
    if not campos:
        return {"exito": False, "error": "No hay campos para actualizar"}
    
    valores.append(id_docente)
    
    query = f"UPDATE docentes SET {', '.join(campos)} WHERE id_docente = ?"
    
    try:
        ejecutar_modificacion(query, tuple(valores))
        return {"exito": True, "mensaje": "Docente actualizado exitosamente"}
    except Exception as e:
        return {"exito": False, "error": f"Error al actualizar docente: {str(e)}"}


def eliminar_docente(id_docente: int, db_path: str = DB_PATH) -> Dict:
    """Elimina (desactiva) un docente."""
    return actualizar_docente(id_docente, estado="inactivo")


# =============================================================================
# SERVICIO: INSCRIPCIONES
# =============================================================================

def listar_inscripciones(
    estado: str = None,
    id_curso: int = None,
    db_path: str = DB_PATH
) -> List[Dict]:
    """Lista las inscripciones."""
    from models.database import ejecutar_consulta
    
    query = """
        SELECT i.*, e.nombres_completos as nombre_estudiante, 
               e.identificacion, c.nombre as nombre_curso, c.codigo
        FROM inscripciones i
        JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
        JOIN cursos c ON i.id_curso = c.id_curso
    """
    
    condiciones = []
    params = []
    
    if estado:
        condiciones.append("i.estado = ?")
        params.append(estado)
    if id_curso:
        condiciones.append("i.id_curso = ?")
        params.append(id_curso)
    
    if condiciones:
        query += " WHERE " + " AND ".join(condiciones)
    
    query += " ORDER BY i.fecha_inscripcion DESC"
    
    return ejecutar_consulta(query, tuple(params))


def obtener_inscripcion_por_id(id_inscripcion: int, db_path: str = DB_PATH) -> Optional[Dict]:
    """Obtiene una inscripción por su ID."""
    from models.database import ejecutar_consulta
    
    resultados = ejecutar_consulta(
        "SELECT * FROM inscripciones WHERE id_inscripcion = ?",
        (id_inscripcion,)
    )
    return resultados[0] if resultados else None


def actualizar_inscripcion(
    id_inscripcion: int,
    tiene_pdf_cedula: bool = None,
    tiene_pago: bool = None,
    estado: str = None,
    calificacion: float = None,
    estado_certificacion: str = None,
    db_path: str = DB_PATH
) -> Dict:
    """Actualiza una inscripción."""
    from models.database import ejecutar_modificacion
    
    campos = []
    valores = []
    
    if tiene_pdf_cedula is not None:
        campos.append("tiene_pdf_cedula = ?")
        valores.append(tiene_pdf_cedula)
    if tiene_pago is not None:
        campos.append("tiene_pago = ?")
        valores.append(tiene_pago)
    if estado:
        campos.append("estado = ?")
        valores.append(estado)
    if calificacion is not None:
        campos.append("calificacion = ?")
        valores.append(calificacion)
    if estado_certificacion:
        campos.append("estado_certificacion = ?")
        valores.append(estado_certificacion)
    
    if not campos:
        return {"exito": False, "error": "No hay campos para actualizar"}
    
    valores.append(id_inscripcion)
    
    query = f"UPDATE inscripciones SET {', '.join(campos)} WHERE id_inscripcion = ?"
    
    try:
        ejecutar_modificacion(query, tuple(valores))
        return {"exito": True, "mensaje": "Inscripción actualizada"}
    except Exception as e:
        return {"exito": False, "error": f"Error: {str(e)}"}


# =============================================================================
# SERVICIO: CERTIFICACIONES
# =============================================================================

def listar_certificaciones(
    estado: str = None,
    db_path: str = DB_PATH
) -> List[Dict]:
    """Lista las certificaciones."""
    from models.database import ejecutar_consulta
    
    query = """
        SELECT cert.*, e.nombres_completos as nombre_estudiante,
               e.identificacion, c.nombre as nombre_curso,
               i.calificacion, i.estado_certificacion
        FROM certificaciones cert
        JOIN inscripciones i ON cert.id_inscripcion = i.id_inscripcion
        JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
        JOIN cursos c ON i.id_curso = c.id_curso
    """
    
    if estado:
        query += " WHERE cert.estado = ?"
        query += " ORDER BY cert.fecha_emision DESC"
        return ejecutar_consulta(query, (estado,))
    
    query += " ORDER BY cert.fecha_emision DESC"
    return ejecutar_consulta(query)


def obtener_certificado_por_id(id_certificacion: int, db_path: str = DB_PATH) -> Optional[Dict]:
    """Obtiene una certificación por su ID."""
    from models.database import ejecutar_consulta
    
    query = """
        SELECT cert.*, e.nombres_completos as nombre_estudiante,
               e.identificacion, c.nombre as nombre_curso,
               i.calificacion, i.estado_certificacion
        FROM certificaciones cert
        JOIN inscripciones i ON cert.id_inscripcion = i.id_inscripcion
        JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
        JOIN cursos c ON i.id_curso = c.id_curso
        WHERE cert.id_certificacion = ?
    """
    
    resultados = ejecutar_consulta(query, (id_certificacion,))
    return resultados[0] if resultados else None


# =============================================================================
# SERVICIO: REPORTES
# =============================================================================

def obtener_estadisticas(db_path: str = DB_PATH) -> Dict:
    """Obtiene estadísticas del sistema."""
    from models.database import ejecutar_consulta
    
    # Total estudiantes
    estudiantes = ejecutar_consulta("SELECT COUNT(*) as total FROM estudiantes WHERE estado = 'activo'")
    total_estudiantes = estudiantes[0]['total'] if estudiantes else 0
    
    # Total cursos
    cursos = ejecutar_consulta("SELECT COUNT(*) as total FROM cursos WHERE estado IN ('activo', 'en_curso')")
    total_cursos = cursos[0]['total'] if cursos else 0
    
    # Total inscripciones activas
    inscripciones = ejecutar_consulta("SELECT COUNT(*) as total FROM inscripciones WHERE estado = 'inscrito'")
    total_inscripciones = inscripciones[0]['total'] if inscripciones else 0
    
    # Total certificados emitidos
    certs = ejecutar_consulta("SELECT COUNT(*) as total FROM certificaciones WHERE estado = 'emitido'")
    total_certificados = certs[0]['total'] if certs else 0
    
    # Docentes activos
    docentes = ejecutar_consulta("SELECT COUNT(*) as total FROM docentes WHERE estado = 'activo'")
    total_docentes = docentes[0]['total'] if docentes else 0
    
    # Cursos con más inscripciones
    cursos_populares = ejecutar_consulta("""
        SELECT c.nombre, COUNT(i.id_inscripcion) as total
        FROM cursos c
        LEFT JOIN inscripciones i ON c.id_curso = i.id_curso AND i.estado = 'inscrito'
        GROUP BY c.id_curso
        ORDER BY total DESC
        LIMIT 5
    """)
    
    return {
        "total_estudiantes": total_estudiantes,
        "total_cursos": total_cursos,
        "total_inscripciones": total_inscripciones,
        "total_certificados": total_certificados,
        "total_docentes": total_docentes,
        "cursos_populares": cursos_populares
    }


# =============================================================================
# SERVICIO: EXPORTACIÓN DE DATOS
# =============================================================================

def exportar_estudiantes_csv(db_path: str = DB_PATH) -> str:
    """
    Exporta todos los estudiantes a formato CSV.
    
    Returns:
        str: Contenido CSV
    """
    from models.database import ejecutar_consulta
    
    estudiantes = ejecutar_consulta(
        "SELECT identificacion, nombres_completos, telefono_fijo, celular, correo_electronico, estado FROM estudiantes ORDER BY nombres_completos"
    )
    
    csv = "identificacion,nombres_completos,telefono_fijo,celular,correo_electronico,estado\n"
    for est in estudiantes:
        csv += f'{est["identificacion"]},{est["nombres_completos"]},{est["telefono_fijo"] or ""},{est["celular"]},{est["correo_electronico"]},{est["estado"]}\n'
    
    return csv


def exportar_cursos_csv(db_path: str = DB_PATH) -> str:
    """Exporta todos los cursos a formato CSV."""
    from models.database import ejecutar_consulta
    
    cursos = ejecutar_consulta(
        "SELECT codigo, nombre, modalidad, fecha_inicio, fecha_fin, inversion, estado FROM cursos ORDER BY nombre"
    )
    
    csv = "codigo,nombre,modalidad,fecha_inicio,fecha_fin,inversion,estado\n"
    for cur in cursos:
        csv += f'{cur["codigo"]},{cur["nombre"]},{cur["modalidad"]},{cur["fecha_inicio"]},{cur["fecha_fin"]},{cur["inversion"]},{cur["estado"]}\n'
    
    return csv


def exportar_inscripciones_csv(db_path: str = DB_PATH) -> str:
    """Exporta todas las inscripciones a formato CSV."""
    from models.database import ejecutar_consulta
    
    query = """
        SELECT e.identificacion, e.nombres_completos, c.nombre as curso,
               i.fecha_inscripcion, i.tiene_pdf_cedula, i.tiene_pago,
               i.estado_certificacion, i.calificacion, i.estado
        FROM inscripciones i
        JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
        JOIN cursos c ON i.id_curso = c.id_curso
        ORDER BY i.fecha_inscripcion DESC
    """
    inscripciones = ejecutar_consulta(query)
    
    csv = "identificacion,estudiante,curso,fecha_inscripcion,tiene_pdf_cedula,tiene_pago,estado_certificacion,calificacion,estado\n"
    for ins in inscripciones:
        csv += f'{ins["identificacion"]},{ins["nombres_completos"]},{ins["curso"]},{ins["fecha_inscripcion"]},{ins["tiene_pdf_cedula"]},{ins["tiene_pago"]},{ins["estado_certificacion"]},{ins["calificacion"] or ""},{ins["estado"]}\n'
    
    return csv


# =============================================================================
# SERVICIO: BÚSQUEDA
# =============================================================================

def buscar_estudiantes(texto: str, db_path: str = DB_PATH) -> List[Dict]:
    """
    Busca estudiantes por nombre, cédula o correo.
    
    Args:
        texto: Texto de búsqueda
    
    Returns:
        List[Dict]: Lista de estudiantes que coinciden
    """
    from models.database import ejecutar_consulta
    
    patron = f"%{texto}%"
    query = """
        SELECT * FROM estudiantes 
        WHERE nombres_completos LIKE ? OR identificacion LIKE ? OR correo_electronico LIKE ?
        ORDER BY nombres_completos
    """
    return ejecutar_consulta(query, (patron, patron, patron))


def buscar_cursos(texto: str, db_path: str = DB_PATH) -> List[Dict]:
    """Busca cursos por nombre o código."""
    from models.database import ejecutar_consulta
    
    patron = f"%{texto}%"
    query = """
        SELECT * FROM cursos 
        WHERE nombre LIKE ? OR codigo LIKE ?
        ORDER BY nombre
    """
    return ejecutar_consulta(query, (patron, patron))


# =============================================================================
# END OF FILE
# =============================================================================