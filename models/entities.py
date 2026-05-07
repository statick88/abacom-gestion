"""
================================================================================
ENTIDADES DEL SISTEMA - ORIENTACIÓN A OBJETOS
================================================================================
Evolución de programación funcional a OOP.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pathlib import Path
import sys

# Agregar el directorio raíz al path
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))


@dataclass
class Estudiante:
    """
    Representa a un estudiante en el sistema de gestión educativa.

    Attributes:
        id_estudiante: Identificador único en la base de datos.
        identificacion: Cédula de identidad (10 dígitos Ecuador).
        nombres_completos: Nombres completos del estudiante.
        telefono_fijo: Teléfono fijo (opcional).
        celular: Número de celular.
        correo_electronico: Correo electrónico.
        direccion: Dirección de domicilio (opcional).
        fecha_nacimiento: Fecha de nacimiento (opcional).
        estado: Estado del estudiante ('activo', 'inactivo', 'egresado').

    Example:
        >>> est = Estudiante(
        ...     identificacion="1712345678",
        ...     nombres_completos="Juan Pérez",
        ...     celular="0991234567",
        ...     correo_electronico="juan@email.com"
        ... )
    """
    identificacion: str = ""
    nombres_completos: str = ""
    telefono_fijo: Optional[str] = None
    celular: str = ""
    correo_electronico: str = ""
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    estado: str = "activo"
    id_estudiante: Optional[int] = field(default=None, repr=False)

    def validar_cedula(self) -> bool:
        """
        Valida que la cédula tenga formato válido para Ecuador.

        Returns:
            bool: True si la cédula es válida, False en caso contrario.

        Raises:
            ImportError: Si el módulo de validación no está disponible.
        """
        from services.validacion.cedula import validar_cedula_ecuador
        return validar_cedula_ecuador(self.identificacion)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto a diccionario para persistencia.

        Returns:
            Dict con todos los atributos del estudiante.
        """
        return {
            "id_estudiante": self.id_estudiante,
            "identificacion": self.identificacion,
            "nombres_completos": self.nombres_completos,
            "telefono_fijo": self.telefono_fijo,
            "celular": self.celular,
            "correo_electronico": self.correo_electronico,
            "direccion": self.direccion,
            "fecha_nacimiento": self.fecha_nacimiento,
            "estado": self.estado,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Estudiante":
        """
        Crea una instancia de Estudiante desde un diccionario.

        Args:
            datos: Diccionario con los datos del estudiante.

        Returns:
            Nueva instancia de Estudiante.
        """
        return cls(
            id_estudiante=data.get("id_estudiante"),
            identificacion=data.get("identificacion", ""),
            nombres_completos=data.get("nombres_completos", ""),
            telefono_fijo=data.get("telefono_fijo"),
            celular=data.get("celular", ""),
            correo_electronico=data.get("correo_electronico", ""),
            direccion=data.get("direccion"),
            fecha_nacimiento=data.get("fecha_nacimiento"),
            estado=data.get("estado", "activo"),
        )

    def __str__(self) -> str:
        """Representación en string del estudiante."""
        return f"Estudiante: {self.nombres_completos} (C.I: {self.identificacion})"


@dataclass
class Curso:
    """
    Representa un curso en el sistema de gestión educativa.

    Attributes:
        id_curso: Identificador único en la base de datos.
        codigo: Código identificador del curso (ej: '01').
        nombre: Nombre del curso.
        modalidad: Modalidad ('Online', 'Virtual', 'Presencial').
        fecha_inicio: Fecha de inicio (YYYY-MM-DD).
        fecha_fin: Fecha de fin (YYYY-MM-DD).
        horario_inicio: Hora de inicio (HH:MM).
        horario_fin: Hora de fin (HH:MM).
        dias_semana: Días de clase (ej: 'Lunes,Miércoles').
        inversion: Costo del curso.
        id_docente: ID del docente asignado.
        capacidad: Cupo máximo de estudiantes.
        estado: Estado del curso.
        periodo_academico: Período académico (año).

    Example:
        >>> curso = Curso(
        ...     codigo="01",
        ...     nombre="Python Básico",
        ...     modalidad="Online",
        ...     fecha_inicio="2026-01-01",
        ...     fecha_fin="2026-03-01",
        ...     horario_inicio="19:00",
        ...     horario_fin="22:00",
        ...     dias_semana="Lunes,Miércoles",
        ...     inversion=150.0
        ... )
    """
    codigo: str = ""
    nombre: str = ""
    modalidad: str = "Online"
    fecha_inicio: str = ""
    fecha_fin: str = ""
    horario_inicio: str = ""
    horario_fin: str = ""
    dias_semana: str = ""
    inversion: float = 0.0
    id_docente: Optional[int] = None
    capacidad: int = 30
    estado: str = "activo"
    periodo_academico: int = 2026
    id_curso: Optional[int] = field(default=None, repr=False)

    def calcular_duracion_semanas(self) -> int:
        """
        Calcula la duración del curso en semanas.

        Returns:
            int: Número de semanas entre fecha_inicio y fecha_fin.

        Raises:
            ValueError: Si el formato de fecha es inválido.
        """
        try:
            inicio = datetime.strptime(self.fecha_inicio, "%Y-%m-%d")
            fin = datetime.strptime(self.fecha_fin, "%Y-%m-%d")
            return (fin - inicio).days // 7
        except ValueError:
            return 0

    def calcular_hora_notificacion(self) -> str:
        """
        Calcula la hora de notificación (30 minutos antes de clase).

        Returns:
            str: Hora en formato HH:MM para enviar notificación.
        """
        from services.notificaciones.notificador import (
            calcular_hora_notificacion,
        )

        return calcular_hora_notificacion(self.horario_inicio)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto a diccionario para persistencia.

        Returns:
            Dict con todos los atributos del curso.
        """
        return {
            "id_curso": self.id_curso,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "modalidad": self.modalidad,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "horario_inicio": self.horario_inicio,
            "horario_fin": self.horario_fin,
            "dias_semana": self.dias_semana,
            "inversion": self.inversion,
            "id_docente": self.id_docente,
            "capacidad": self.capacidad,
            "estado": self.estado,
            "periodo_academico": self.periodo_academico,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Curso":
        """
        Crea una instancia de Curso desde un diccionario.

        Args:
            data: Diccionario con los datos del curso.

        Returns:
            Nueva instancia de Curso.
        """
        return cls(
            id_curso=data.get("id_curso"),
            codigo=data.get("codigo", ""),
            nombre=data.get("nombre", ""),
            modalidad=data.get("modalidad", "Online"),
            fecha_inicio=data.get("fecha_inicio", ""),
            fecha_fin=data.get("fecha_fin", ""),
            horario_inicio=data.get("horario_inicio", ""),
            horario_fin=data.get("horario_fin", ""),
            dias_semana=data.get("dias_semana", ""),
            inversion=data.get("inversion", 0.0),
            id_docente=data.get("id_docente"),
            capacidad=data.get("capacidad", 30),
            estado=data.get("estado", "activo"),
            periodo_academico=data.get("periodo_academico", 2026),
        )

    def __str__(self) -> str:
        """Representación en string del curso."""
        return f"Curso: {self.nombre} ({self.codigo})"


@dataclass
class Inscripcion:
    """
    Representa una inscripción de un estudiante a un curso.

    Attributes:
        id_inscripcion: Identificador único en la base de datos.
        id_estudiante: ID del estudiante.
        id_curso: ID del curso.
        fecha_inscripcion: Fecha de inscripción.
        tiene_pdf_cedula: Indica si entregó PDF de cédula.
        ruta_pdf_cedula: Ruta del archivo PDF.
        tiene_pago: Indica si tiene comprobante de pago.
        comprobante_pago: Ruta del comprobante.
        estado_certificacion: Estado de certificación.
        calificacion: Calificación obtained (opcional).
        observaciones: Observaciones adicionales.
        estado: Estado de la inscripción.
    """
    id_estudiante: int = 0
    id_curso: int = 0
    fecha_inscripcion: Optional[str] = None
    tiene_pdf_cedula: bool = False
    ruta_pdf_cedula: Optional[str] = None
    tiene_pago: bool = False
    comprobante_pago: Optional[str] = None
    estado_certificacion: str = "pendiente"
    calificacion: Optional[float] = None
    observaciones: Optional[str] = None
    estado: str = "inscrito"
    id_inscripcion: Optional[int] = field(default=None, repr=False)
    _estudiante: Optional[Estudiante] = field(default=None, repr=False)
    _curso: Optional[Curso] = field(default=None, repr=False)

    def validar_requisitos(self) -> Dict[str, Any]:
        """
        Valida los requisitos de la inscripción.

        Returns:
            Dict con 'valida' (bool) y 'errores' (list).
        """
        errores: List[str] = []

        if not self.tiene_pdf_cedula:
            errores.append("Falta copia de cédula en PDF")

        if not self.tiene_pago:
            errores.append("Falta comprobante de pago")

        return {
            "valida": len(errores) == 0,
            "errores": errores,
        }

    def get_estudiante(self) -> Optional[Estudiante]:
        """
        Obtiene el estudiante relacionado mediante lazy loading.

        Returns:
            Estudiante si existe, None en caso contrario.
        """
        if self._estudiante is None:
            from models.database import ejecutar_consulta

            resultados = ejecutar_consulta(
                "SELECT * FROM estudiantes WHERE id_estudiante = ?",
                (self.id_estudiante,),
            )
            if resultados:
                self._estudiante = Estudiante.from_dict(resultados[0])
        return self._estudiante

    def get_curso(self) -> Optional[Curso]:
        """
        Obtiene el curso relacionado mediante lazy loading.

        Returns:
            Curso si existe, None en caso contrario.
        """
        if self._curso is None:
            from models.database import ejecutar_consulta

            resultados = ejecutar_consulta(
                "SELECT * FROM cursos WHERE id_curso = ?", (self.id_curso,)
            )
            if resultados:
                self._curso = Curso.from_dict(resultados[0])
        return self._curso

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto a diccionario para persistencia.

        Returns:
            Dict con todos los atributos de la inscripción.
        """
        return {
            "id_inscripcion": self.id_inscripcion,
            "id_estudiante": self.id_estudiante,
            "id_curso": self.id_curso,
            "fecha_inscripcion": self.fecha_inscripcion,
            "tiene_pdf_cedula": self.tiene_pdf_cedula,
            "ruta_pdf_cedula": self.ruta_pdf_cedula,
            "tiene_pago": self.tiene_pago,
            "comprobante_pago": self.comprobante_pago,
            "estado_certificacion": self.estado_certificacion,
            "calificacion": self.calificacion,
            "observaciones": self.observaciones,
            "estado": self.estado,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Inscripcion":
        """
        Crea una instancia de Inscripcion desde un diccionario.

        Args:
            data: Diccionario con los datos de la inscripción.

        Returns:
            Nueva instancia de Inscripcion.
        """
        return cls(
            id_inscripcion=data.get("id_inscripcion"),
            id_estudiante=data.get("id_estudiante", 0),
            id_curso=data.get("id_curso", 0),
            fecha_inscripcion=data.get("fecha_inscripcion"),
            tiene_pdf_cedula=data.get("tiene_pdf_cedula", False),
            ruta_pdf_cedula=data.get("ruta_pdf_cedula"),
            tiene_pago=data.get("tiene_pago", False),
            comprobante_pago=data.get("comprobante_pago"),
            estado_certificacion=data.get("estado_certificacion", "pendiente"),
            calificacion=data.get("calificacion"),
            observaciones=data.get("observaciones"),
            estado=data.get("estado", "inscrito"),
        )

    def __str__(self) -> str:
        """Representación en string de la inscripción."""
        return (
            f"Inscripción #{self.id_inscripcion} - "
            f"Estudiante: {self.id_estudiante}, Curso: {self.id_curso}"
        )


@dataclass
class Certificado:
    """
    Representa un certificado de aprobación emitido por el sistema.

    Attributes:
        id_certificacion: Identificador único.
        id_inscripcion: ID de la inscripción relacionada.
        numero_certificado: Número único del certificado.
        fecha_emision: Fecha de emisión (YYYY-MM-DD).
        estado: Estado ('emitido', 'entregado', 'anulado').
        aval_ministerio: Aval del Ministerio del Trabajo.
    """
    id_inscripcion: int = 0
    numero_certificado: str = ""
    fecha_emision: Optional[str] = None
    estado: str = "emitido"
    aval_ministerio: Optional[str] = None
    id_certificacion: Optional[int] = field(default=None, repr=False)
    _inscripcion: Optional[Inscripcion] = field(default=None, repr=False)

    def generar_pdf(self) -> str:
        """
        Genera el PDF del certificado.

        Returns:
            str: Ruta del archivo PDF generado, o string vacío si falla.
        """
        from services.pdf.generator import generar_certificado_pdf

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
            fecha_emision=self.fecha_emision
            or datetime.now().strftime("%Y-%m-%d"),
        )

    def get_inscripcion(self) -> Optional[Inscripcion]:
        """
        Obtiene la inscripción relacionada mediante lazy loading.

        Returns:
            Inscripcion si existe, None en caso contrario.
        """
        if self._inscripcion is None:
            from models.database import ejecutar_consulta

            resultados = ejecutar_consulta(
                "SELECT * FROM inscripciones WHERE id_inscripcion = ?",
                (self.id_inscripcion,),
            )
            if resultados:
                self._inscripcion = Inscripcion.from_dict(resultados[0])
        return self._inscripcion

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto a diccionario para persistencia.

        Returns:
            Dict con todos los atributos del certificado.
        """
        return {
            "id_certificacion": self.id_certificacion,
            "id_inscripcion": self.id_inscripcion,
            "numero_certificado": self.numero_certificado,
            "fecha_emision": self.fecha_emision,
            "estado": self.estado,
            "aval_ministerio": self.aval_ministerio,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Certificado":
        """
        Crea una instancia de Certificado desde un diccionario.

        Args:
            data: Diccionario con los datos del certificado.

        Returns:
            Nueva instancia de Certificado.
        """
        return cls(
            id_certificacion=data.get("id_certificacion"),
            id_inscripcion=data.get("id_inscripcion", 0),
            numero_certificado=data.get("numero_certificado", ""),
            fecha_emision=data.get("fecha_emision"),
            estado=data.get("estado", "emitido"),
            aval_ministerio=data.get("aval_ministerio"),
        )

    def __str__(self) -> str:
        """Representación en string del certificado."""
        return f"Certificado: {self.numero_certificado} ({self.estado})"