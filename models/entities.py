"""
================================================================================
ENTIDADES DEL SISTEMA - ORIENTACIÓN A OBJETOS
================================================================================
Evolución de programación funcional a OOP.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from datetime import datetime, date
from typing import Optional, List, Dict
from decimal import Decimal

# =============================================================================
# CLASE: ESTUDIANTE
# =============================================================================

class Estudiante:
    """Representa a un estudiante en el sistema."""
    
    def __init__(
        self,
        id_estudiante: Optional[int] = None,
        identificacion: str = "",
        nombres_completos: str = "",
        telefono_fijo: Optional[str] = None,
        celular: str = "",
        correo_electronico: str = "",
        direccion: Optional[str] = None,
        fecha_nacimiento: Optional[str] = None,
        estado: str = "activo"
    ):
        self.id_estudiante = id_estudiante
        self.identificacion = identificacion
        self.nombres_completos = nombres_completos
        self.telefono_fijo = telefono_fijo
        self.celular = celular
        self.correo_electronico = correo_electronico
        self.direccion = direccion
        self.fecha_nacimiento = fecha_nacimiento
        self.estado = estado
    
    def validar_cedula(self) -> bool:
        """Valida que la cédula tenga formato válido."""
        from services.servicios import validar_cedula_ecuador
        return validar_cedula_ecuador(self.identificacion)
    
    def to_dict(self) -> Dict:
        """Convierte el objeto a diccionario."""
        return {
            'id_estudiante': self.id_estudiante,
            'identificacion': self.identificacion,
            'nombres_completos': self.nombres_completos,
            'telefono_fijo': self.telefono_fijo,
            'celular': self.celular,
            'correo_electronico': self.correo_electronico,
            'direccion': self.direccion,
            'fecha_nacimiento': self.fecha_nacimiento,
            'estado': self.estado
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Estudiante':
        """Crea un Estudiante desde un diccionario."""
        return cls(
            id_estudiante=data.get('id_estudiante'),
            identificacion=data.get('identificacion', ''),
            nombres_completos=data.get('nombres_completos', ''),
            telefono_fijo=data.get('telefono_fijo'),
            celular=data.get('celular', ''),
            correo_electronico=data.get('correo_electronico', ''),
            direccion=data.get('direccion'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            estado=data.get('estado', 'activo')
        )
    
    def __str__(self):
        return f"Estudiante: {self.nombres_completos} (C.I: {self.identificacion})"


# =============================================================================
# CLASE: CURSO
# =============================================================================

class Curso:
    """Representa un curso en el sistema."""
    
    def __init__(
        self,
        id_curso: Optional[int] = None,
        codigo: str = "",
        nombre: str = "",
        modalidad: str = "Online",
        fecha_inicio: str = "",
        fecha_fin: str = "",
        horario_inicio: str = "",
        horario_fin: str = "",
        dias_semana: str = "",
        inversion: float = 0.0,
        id_docente: Optional[int] = None,
        capacidad: int = 30,
        estado: str = "activo",
        periodo_academico: int = 2026
    ):
        self.id_curso = id_curso
        self.codigo = codigo
        self.nombre = nombre
        self.modalidad = modalidad
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.horario_inicio = horario_inicio
        self.horario_fin = horario_fin
        self.dias_semana = dias_semana
        self.inversion = inversion
        self.id_docente = id_docente
        self.capacidad = capacidad
        self.estado = estado
        self.periodo_academico = periodo_academico
    
    def calcular_duracion_semanas(self) -> int:
        """Calcula la duración en semanas."""
        from datetime import datetime
        inicio = datetime.strptime(self.fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(self.fecha_fin, "%Y-%m-%d")
        return (fin - inicio).days // 7
    
    def calcular_hora_notificacion(self) -> str:
        """Calcula la hora de notificación (30 min antes)."""
        from services.servicios import calcular_hora_notificacion
        return calcular_hora_notificacion(self.horario_inicio)
    
    def to_dict(self) -> Dict:
        """Convierte el objeto a diccionario."""
        return {
            'id_curso': self.id_curso,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'modalidad': self.modalidad,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'horario_inicio': self.horario_inicio,
            'horario_fin': self.horario_fin,
            'dias_semana': self.dias_semana,
            'inversion': self.inversion,
            'id_docente': self.id_docente,
            'capacidad': self.capacidad,
            'estado': self.estado,
            'periodo_academico': self.periodo_academico
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Curso':
        """Crea un Curso desde un diccionario."""
        return cls(
            id_curso=data.get('id_curso'),
            codigo=data.get('codigo', ''),
            nombre=data.get('nombre', ''),
            modalidad=data.get('modalidad', 'Online'),
            fecha_inicio=data.get('fecha_inicio', ''),
            fecha_fin=data.get('fecha_fin', ''),
            horario_inicio=data.get('horario_inicio', ''),
            horario_fin=data.get('horario_fin', ''),
            dias_semana=data.get('dias_semana', ''),
            inversion=data.get('inversion', 0.0),
            id_docente=data.get('id_docente'),
            capacidad=data.get('capacidad', 30),
            estado=data.get('estado', 'activo'),
            periodo_academico=data.get('periodo_academico', 2026)
        )
    
    def __str__(self):
        return f"Curso: {self.nombre} ({self.codigo})"


# =============================================================================
# CLASE: INSCRIPCION
# =============================================================================

class Inscripcion:
    """Representa una inscripción en el sistema."""
    
    def __init__(
        self,
        id_inscripcion: Optional[int] = None,
        id_estudiante: int = 0,
        id_curso: int = 0,
        fecha_inscripcion: Optional[str] = None,
        tiene_pdf_cedula: bool = False,
        ruta_pdf_cedula: Optional[str] = None,
        tiene_pago: bool = False,
        comprobante_pago: Optional[str] = None,
        estado_certificacion: str = "pendiente",
        calificacion: Optional[float] = None,
        observaciones: Optional[str] = None,
        estado: str = "inscrito"
    ):
        self.id_inscripcion = id_inscripcion
        self.id_estudiante = id_estudiante
        self.id_curso = id_curso
        self.fecha_inscripcion = fecha_inscripcion
        self.tiene_pdf_cedula = tiene_pdf_cedula
        self.ruta_pdf_cedula = ruta_pdf_cedula
        self.tiene_pago = tiene_pago
        self.comprobante_pago = comprobante_pago
        self.estado_certificacion = estado_certificacion
        self.calificacion = calificacion
        self.observaciones = observaciones
        self.estado = estado
        
        # Objetos relacionados (lazy loading)
        self._estudiante = None
        self._curso = None
    
    def validar_requisitos(self) -> Dict:
        """Valida los requisitos de la inscripción."""
        errores = []
        
        if not self.tiene_pdf_cedula:
            errores.append("Falta copia de cédula en PDF")
        
        if not self.tiene_pago:
            errores.append("Falta comprobante de pago")
        
        return {
            "valida": len(errores) == 0,
            "errores": errores
        }
    
    def get_estudiante(self):
        """Obtiene el estudiante relacionado."""
        if self._estudiante is None:
            from services.servicios import obtener_estudiante_por_cedula
            from models.database import ejecutar_consulta
            resultados = ejecutar_consulta(
                "SELECT * FROM estudiantes WHERE id_estudiante = ?",
                (self.id_estudiante,)
            )
            if resultados:
                self._estudiante = Estudiante.from_dict(resultados[0])
        return self._estudiante
    
    def get_curso(self):
        """Obtiene el curso relacionado."""
        if self._curso is None:
            from models.database import ejecutar_consulta
            resultados = ejecutar_consulta(
                "SELECT * FROM cursos WHERE id_curso = ?",
                (self.id_curso,)
            )
            if resultados:
                self._curso = Curso.from_dict(resultados[0])
        return self._curso
    
    def to_dict(self) -> Dict:
        """Convierte el objeto a diccionario."""
        return {
            'id_inscripcion': self.id_inscripcion,
            'id_estudiante': self.id_estudiante,
            'id_curso': self.id_curso,
            'fecha_inscripcion': self.fecha_inscripcion,
            'tiene_pdf_cedula': self.tiene_pdf_cedula,
            'ruta_pdf_cedula': self.ruta_pdf_cedula,
            'tiene_pago': self.tiene_pago,
            'comprobante_pago': self.comprobante_pago,
            'estado_certificacion': self.estado_certificacion,
            'calificacion': self.calificacion,
            'observaciones': self.observaciones,
            'estado': self.estado
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Inscripcion':
        """Crea una Inscripcion desde un diccionario."""
        return cls(
            id_inscripcion=data.get('id_inscripcion'),
            id_estudiante=data.get('id_estudiante', 0),
            id_curso=data.get('id_curso', 0),
            fecha_inscripcion=data.get('fecha_inscripcion'),
            tiene_pdf_cedula=data.get('tiene_pdf_cedula', False),
            ruta_pdf_cedula=data.get('ruta_pdf_cedula'),
            tiene_pago=data.get('tiene_pago', False),
            comprobante_pago=data.get('comprobante_pago'),
            estado_certificacion=data.get('estado_certificacion', 'pendiente'),
            calificacion=data.get('calificacion'),
            observaciones=data.get('observaciones'),
            estado=data.get('estado', 'inscrito')
        )
    
    def __str__(self):
        return f"Inscripción #{self.id_inscripcion} - Estudiante: {self.id_estudiante}, Curso: {self.id_curso}"


# =============================================================================
# CLASE: CERTIFICADO
# =============================================================================

class Certificado:
    """Representa un certificado en el sistema."""
    
    def __init__(
        self,
        id_certificacion: Optional[int] = None,
        id_inscripcion: int = 0,
        numero_certificado: str = "",
        fecha_emision: Optional[str] = None,
        estado: str = "emitido",
        aval_ministerio: Optional[str] = None
    ):
        self.id_certificacion = id_certificacion
        self.id_inscripcion = id_inscripcion
        self.numero_certificado = numero_certificado
        self.fecha_emision = fecha_emision
        self.estado = estado
        self.aval_ministerio = aval_ministerio
        
        # Objeto relacionado (lazy loading)
        self._inscripcion = None
    
    def generar_pdf(self) -> str:
        """Genera el PDF del certificado."""
        from services.pdf_generator import generar_certificado_pdf
        
        inscripcion = self.get_inscripcion()
        if not inscripcion:
            return ""
        
        estudiante = inscripcion.get_estudiante()
        curso = inscripcion.get_curso()
        
        if not estudiante or not curso:
            return ""
        
        return generar_certificado_pdf(
            numero_certificado=self.numero_certificado,
            nombre_estudiante=estudiante.nombres_completos,
            nombre_curso=curso.nombre,
            calificacion=inscripcion.calificacion or 0.0,
            fecha_emision=self.fecha_emision or datetime.now().strftime('%Y-%m-%d')
        )
    
    def get_inscripcion(self):
        """Obtiene la inscripción relacionada."""
        if self._inscripcion is None:
            from models.database import ejecutar_consulta
            resultados = ejecutar_consulta(
                "SELECT * FROM inscripciones WHERE id_inscripcion = ?",
                (self.id_inscripcion,)
            )
            if resultados:
                self._inscripcion = Inscripcion.from_dict(resultados[0])
        return self._inscripcion
    
    def to_dict(self) -> Dict:
        """Convierte el objeto a diccionario."""
        return {
            'id_certificacion': self.id_certificacion,
            'id_inscripcion': self.id_inscripcion,
            'numero_certificado': self.numero_certificado,
            'fecha_emision': self.fecha_emision,
            'estado': self.estado,
            'aval_ministerio': self.aval_ministerio
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Certificado':
        """Crea un Certificado desde un diccionario."""
        return cls(
            id_certificacion=data.get('id_certificacion'),
            id_inscripcion=data.get('id_inscripcion', 0),
            numero_certificado=data.get('numero_certificado', ''),
            fecha_emision=data.get('fecha_emision'),
            estado=data.get('estado', 'emitido'),
            aval_ministerio=data.get('aval_ministerio')
        )
    
    def __str__(self):
        return f"Certificado: {self.numero_certificado} ({self.estado})"


# =============================================================================
# END OF FILE
# =============================================================================
