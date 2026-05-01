"""
Especificaciones del Sistema de Gestión Educativa ABACOM
=========================================================
Casos de prueba que validan las reglas de negocio del sistema.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
Enfoque: Spec-Driven Development (SDD)
"""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal


# =============================================================================
# ESPECIFICACIONES - REGLAS DE NEGOCIO
# =============================================================================

class SpecEstudiante:
    """
    Especificación: Validación de estudiante por Cédula de Identidad Ecuador
    ----------------------------------------------------
    Dado un número de cédula de Ecuador (10 dígitos)
    Cuando se verifica el formato
    Entonces debe ser válido para registro en el sistema
    """

    @staticmethod
    def validar_cedula(cedula: str) -> bool:
        """
        Valida que la cédula tenga formato válido para Ecuador.
        - Longitud exacta: 10 dígitos
        - Primeros 2 dígitos deben estar entre 01-24 (código provincia)
        """
        if not cedula or not isinstance(cedula, str):
            return False

        # Remover espacios y guiones
        cedula_limpia = cedula.replace(" ", "").replace("-", "")

        # Verificar que sean exactamente 10 dígitos
        if len(cedula_limpia) != 10:
            return False

        if not cedula_limpia.isdigit():
            return False

        # Validar código de provincia (01-24)
        provincia = int(cedula_limpia[:2])
        if provincia < 1 or provincia > 24:
            return False

        return True


class SpecCurso:
    """
    Especificación: Gestión de cursos con período académico
    ---------------------------------------------------
    Dado un curso con fecha de inicio
    Cuando se asignan estudiantes
    Entonces deben pertenecer al período académico correspondiente (ej. 2026)
    """

    @staticmethod
    def validar_periodo(fecha_inicio: datetime, periodo: int) -> bool:
        """
        Valida que la fecha de inicio corresponda al período académico.
        """
        return fecha_inicio.year == periodo

    @staticmethod
    def calcular_duracion_semanas(fecha_inicio: datetime, fecha_fin: datetime) -> int:
        """Calcula la duración en semanas del curso."""
        delta = fecha_fin - fecha_inicio
        return delta.days // 7


class SpecInscripcion:
    """
    Especificación: Registro de inscripción con requisitos
    -----------------------------------------------------
    Dado un estudiante que se inscribe a un curso
    Cuando se registra la inscripción
    Entonces debe validar:
    - Copia de cédula en PDF
    - Comprobante de pago
    - Estado de certificación (Aprobado con aval Ministerio Trabajo)
    """

    @staticmethod
    def validar_inscripcion(
        cedula_estudiante: str,
        tiene_pdf_cedula: bool,
        tiene_pago: bool,
        estado_certificacion: str
    ) -> dict:
        """
        Valida que la inscripción cumpla todos los requisitos.
        Retorna dict con 'valida' y lista de errores.
        """
        errores = []

        # Validar Cédula
        if not SpecEstudiante.validar_cedula(cedula_estudiante):
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


class SpecNotificacion:
    """
    Especificación: Sistema de notificaciones con política estricta
    --------------------------------------------------------------
    Dado un curso con horario (ej. 19:00-22:00)
    Cuando se genera la notificación para clase en vivo
    Entonces debe enviarse exactamente 30 minutos antes (18:30)
    """

    @staticmethod
    def calcular_hora_notificacion(hora_inicio: str) -> datetime:
        """
        Calcula la hora exacta de envío de notificación.
        Política: 30 minutos antes de la hora de inicio.
        """
        hora_objeto = datetime.strptime(hora_inicio, "%H:%M")
        hora_notificacion = hora_objeto - timedelta(minutes=30)
        return hora_notificacion

    @staticmethod
    def debe_enviar_notificacion(
        hora_actual: datetime,
        hora_inicio_clase: datetime
    ) -> bool:
        """
        Determina si debe enviarse la notificación.
        Política estricta: solo cuando hora_actual == hora_notificacion (30 min antes)
        """
        hora_notificacion = hora_inicio_clase - timedelta(minutes=30)

        # Comparar solo hora y minuto (ignorar segundos)
        return (
            hora_actual.hour == hora_notificacion.hour and
            hora_actual.minute == hora_notificacion.minute
        )


class SpecCertificacion:
    """
    Especificación: Estado de certificación con aval del Ministerio
    ---------------------------------------------------------------
    Dado un estudiante que completa un curso
    Cuando se genera el certificado
    Entonces debe indicar:
    - Estado: APROBACIÓN
    - Aval: Ministerio del Trabajo (para certificación oficial)
    """

    @staticmethod
    def generar_certificado(
        nombre_estudiante: str,
        nombre_curso: str,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        calificacion: float
    ) -> dict:
        """
        Genera los datos del certificado.
        Requiere aval del Ministerio del Trabajo para certificación oficial.
        """
        if calificacion < 70:
            estado = "REPROBADO"
            aval = None
        else:
            estado = "APROBACIÓN"
            # Aval del Ministerio del Trabajo se incluye automáticamente
            aval = "Ministerio del Trabajo - Ecuador"

        return {
            "estudiante": nombre_estudiante,
            "curso": nombre_curso,
            "fecha_inicio": fecha_inicio.strftime("%d/%m/%Y"),
            "fecha_fin": fecha_fin.strftime("%d/%m/%Y"),
            "calificacion": calificacion,
            "estado": estado,
            "aval_ministerio": aval
        }


# =============================================================================
# PRUEBAS - CASOS DE TEST CON pytest
# =============================================================================

class TestSpecEstudiante:
    """Pruebas para validación de estudiantes por Cédula"""

    def test_cedula_valida_10_digitos(self):
        """Cédula válida de 10 dígitos"""
        assert SpecEstudiante.validar_cedula("1712345678") is True

    def test_cedula_invalida_menos_digitos(self):
        """Cédula con menos de 10 dígitos"""
        assert SpecEstudiante.validar_cedula("171234567") is False

    def test_cedula_invalida_mas_digitos(self):
        """Cédula con más de 10 dígitos"""
        assert SpecEstudiante.validar_cedula("17123456789") is False

    def test_cedula_invalida_provincia(self):
        """Cédula con código de provincia inválido"""
        assert SpecEstudiante.validar_cedula("0012345678") is False

    def test_cedula_invalida_letras(self):
        """Cédula con letras"""
        assert SpecEstudiante.validar_cedula("17ABCD5678") is False

    def test_cedula_vacia(self):
        """Cédula vacía"""
        assert SpecEstudiante.validar_cedula("") is False

    def test_cedula_none(self):
        """Cédula None"""
        assert SpecEstudiante.validar_cedula(None) is False


class TestSpecCurso:
    """Pruebas para gestión de cursos"""

    def test_validar_periodo_2026(self):
        """Curso con fecha en 2026 debe ser válido"""
        fecha = datetime(2026, 4, 13)
        assert SpecCurso.validar_periodo(fecha, 2026) is True

    def test_validar_periodo_invalido(self):
        """Curso con fecha en año diferente al período"""
        fecha = datetime(2025, 4, 13)
        assert SpecCurso.validar_periodo(fecha, 2026) is False

    def test_calcular_duracion_semanas(self):
        """Cálculo correcto de duración en semanas"""
        inicio = datetime(2026, 4, 13)
        fin = datetime(2026, 5, 8)
        assert SpecCurso.calcular_duracion_semanas(inicio, fin) == 3


class TestSpecInscripcion:
    """Pruebas para registro de inscripciones"""

    def test_inscripcion_completa_valida(self):
        """Inscripción con todos los requisitos"""
        resultado = SpecInscripcion.validar_inscripcion(
            cedula_estudiante="1712345678",
            tiene_pdf_cedula=True,
            tiene_pago=True,
            estado_certificacion="aprobado"
        )
        assert resultado["valida"] is True
        assert len(resultado["errores"]) == 0

    def test_inscripcion_sin_pdf_cedula(self):
        """Inscripción sin copia de cédula PDF"""
        resultado = SpecInscripcion.validar_inscripcion(
            cedula_estudiante="1712345678",
            tiene_pdf_cedula=False,
            tiene_pago=True,
            estado_certificacion="aprobado"
        )
        assert resultado["valida"] is False
        assert "copia de cédula" in resultado["errores"][0].lower()

    def test_inscripcion_sin_pago(self):
        """Inscripción sin comprobante de pago"""
        resultado = SpecInscripcion.validar_inscripcion(
            cedula_estudiante="1712345678",
            tiene_pdf_cedula=True,
            tiene_pago=False,
            estado_certificacion="aprobado"
        )
        assert resultado["valida"] is False
        assert "pago" in resultado["errores"][0].lower()

    def test_inscripcion_cedula_invalida(self):
        """Inscripción con cédula inválida"""
        resultado = SpecInscripcion.validar_inscripcion(
            cedula_estudiante="0000000000",
            tiene_pdf_cedula=True,
            tiene_pago=True,
            estado_certificacion="aprobado"
        )
        assert resultado["valida"] is False
        assert "cédula" in resultado["errores"][0].lower()


class TestSpecNotificacion:
    """Pruebas para sistema de notificaciones"""

    def test_hora_notificacion_30_minutos_antes(self):
        """Notificación a las 18:30 para clase a las 19:00"""
        hora_notif = SpecNotificacion.calcular_hora_notificacion("19:00")
        assert hora_notif.hour == 18
        assert hora_notif.minute == 30

    def test_hora_notificacion_clase_22_00(self):
        """Notificación a las 21:30 para clase a las 22:00"""
        hora_notif = SpecNotificacion.calcular_hora_notificacion("22:00")
        assert hora_notif.hour == 21
        assert hora_notif.minute == 30

    def test_debe_enviar_notificacion_exacto(self):
        """Debe enviar cuando es exactamente 30 minutos antes"""
        hora_inicio = datetime(2026, 4, 13, 19, 0, 0)
        hora_actual = datetime(2026, 4, 13, 18, 30, 0)
        assert SpecNotificacion.debe_enviar_notificacion(hora_actual, hora_inicio) is True

    def test_no_enviar_menos_de_30_minutos(self):
        """No enviar si falta menos de 30 minutos"""
        hora_inicio = datetime(2026, 4, 13, 19, 0, 0)
        hora_actual = datetime(2026, 4, 13, 18, 45, 0)
        assert SpecNotificacion.debe_enviar_notificacion(hora_actual, hora_inicio) is False


class TestSpecCertificacion:
    """Pruebas para generación de certificados"""

    def test_certificado_aprobado_con_aval(self):
        """Certificado aprobado con aval del Ministerio"""
        cert = SpecCertificacion.generar_certificado(
            nombre_estudiante="Juan Pérez",
            nombre_curso="Programación con Python",
            fecha_inicio=datetime(2026, 4, 13),
            fecha_fin=datetime(2026, 5, 8),
            calificacion=85.0
        )
        assert cert["estado"] == "APROBACIÓN"
        assert cert["aval_ministerio"] == "Ministerio del Trabajo - Ecuador"

    def test_certificado_reprobado_sin_aval(self):
        """Certificado reprobado sin aval"""
        cert = SpecCertificacion.generar_certificado(
            nombre_estudiante="Juan Pérez",
            nombre_curso="Programación con Python",
            fecha_inicio=datetime(2026, 4, 13),
            fecha_fin=datetime(2026, 5, 8),
            calificacion=60.0
        )
        assert cert["estado"] == "REPROBADO"
        assert cert["aval_ministerio"] is None


# =============================================================================
# PUNTO DE ENTRADA - EJECUTAR PRUEBAS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])