"""
================================================================================
APLICACIÓN DE CONSOLA - SISTEMA DE GESTIÓN ABACOM
================================================================================
Interfaz de línea de comandos para gestionar estudiantes, cursos e inscripciones.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DB_PATH
from services.servicios import (
    validar_cedula_ecuador,
    registrar_estudiante,
    listar_estudiantes,
    obtener_estudiante_por_cedula,
    registrar_curso,
    listar_cursos,
    inscribir_estudiante,
    generar_certificado,
    calcular_hora_notificacion,
    validar_inscripcion
)

from ui.menu import MenuConsola
from ui.handlers import MenuBuilder
from validators.input_helpers import (
    validar_cedula_input,
    validar_numero_input,
    validar_sino_input
)
from formatters.table_formatter import TableFormatter
from formatters.data_formatter import DataFormatter


class AplicacionConsola:
    """Aplicación principal de consola"""

    def __init__(self):
        self.db_path = DB_PATH
        self.menu_principal = None
        self._table_formatter = TableFormatter()
        self._data_formatter = DataFormatter()

    def iniciar(self):
        """Inicia la aplicación"""
        self._construir_menus()
        self._ejecutar_menu_principal()

    def _construir_menus(self):
        """Construye los menús de la aplicación"""
        self.menu_principal = MenuBuilder.build_main_menu(self)

    def _ejecutar_menu_principal(self):
        """Ejecuta el menú principal en bucle"""
        while True:
            self.menu_principal.mostrar()
            opcion = input("\nSeleccione una opción: ").strip()
            if opcion == "0":
                print("\n👋 Gracias por usar el Sistema ABACOM")
                break
            self.menu_principal.ejecutar(opcion)

    # -------------------------------------------------------------------------
    # MENÚ ESTUDIANTES
    # -------------------------------------------------------------------------
    def menu_estudiantes(self):
        """Menú de gestión de estudiantes"""
        menu = MenuBuilder.build_students_menu(self)

        while True:
            menu.mostrar()
            opcion = input("\nSeleccione: ").strip()
            if opcion == "0":
                break
            menu.ejecutar(opcion)

    def _registrar_estudiante(self):
        self._data_formatter.mostrar_encabezado("📝 REGISTRO DE ESTUDIANTE")

        # Validar cédula primero
        cedula = input("Cédula de Identidad (10 dígitos): ").strip()
        if not validar_cedula_input(cedula):
            self._data_formatter.mostrar_error("Cédula inválida. Debe tener 10 dígitos.")
            return

        nombres = input("Nombres Completos: ").strip()
        if not nombres:
            self._data_formatter.mostrar_error("Nombres son requeridos")
            return

        telefono = input("Teléfono Fijo (opcional): ").strip()
        celular = input("Celular: ").strip()
        if not celular:
            self._data_formatter.mostrar_error("Celular es requerido")
            return

        correo = input("Correo Electrónico: ").strip()
        if not correo:
            self._data_formatter.mostrar_error("Correo es requerido")
            return

        # Registrar
        resultado = registrar_estudiante(
            identificacion=cedula,
            nombres_completos=nombres,
            telefono_fijo=telefono or None,
            celular=celular,
            correo_electronico=correo
        )

        if resultado["exito"]:
            self._data_formatter.mostrar_exito(
                resultado['mensaje'],
                {"ID Estudiante": resultado['id_estudiante']}
            )
        else:
            self._data_formatter.mostrar_error(resultado['error'])

    def _buscar_estudiante(self):
        print("\n🔍 BUSCAR ESTUDIANTE POR CÉDULA")
        cedula = input("Ingrese la cédula: ").strip()

        if not validar_cedula_input(cedula):
            self._data_formatter.mostrar_error("Formato de cédula inválido")
            return

        estudiante = obtener_estudiante_por_cedula(cedula)

        if estudiante:
            self._data_formatter.mostrar_estudiante(estudiante)
        else:
            self._data_formatter.mostrar_error("Estudiante no encontrado")

    def _listar_estudiantes(self):
        self._data_formatter.mostrar_encabezado("📋 LISTADO DE ESTUDIANTES", 60)
        estudiantes = listar_estudiantes()
        self._table_formatter.format_estudiantes(estudiantes)

    # -------------------------------------------------------------------------
    # MENÚ CURSOS
    # -------------------------------------------------------------------------
    def menu_cursos(self):
        """Menú de gestión de cursos"""
        menu = MenuBuilder.build_courses_menu(self)

        while True:
            menu.mostrar()
            opcion = input("\nSeleccione: ").strip()
            if opcion == "0":
                break
            menu.ejecutar(opcion)

    def _registrar_curso(self):
        self._data_formatter.mostrar_encabezado("📝 REGISTRO DE CURSO")

        codigo = input("Código (ej. 01): ").strip()
        nombre = input("Nombre del Curso: ").strip()

        print("\nModalidad: 1) Online  2) Virtual  3) Presencial")
        mod_op = input("Seleccione: ").strip()
        modalidades = {"1": "Online", "2": "Virtual", "3": "Presencial"}
        modalidad = modalidades.get(mod_op, "Online")

        fecha_inicio = input("Fecha Inicio (YYYY-MM-DD): ").strip()
        fecha_fin = input("Fecha Fin (YYYY-MM-DD): ").strip()
        hora_inicio = input("Hora Inicio (HH:MM): ").strip()
        hora_fin = input("Hora Fin (HH:MM): ").strip()
        dias = input("Días (ej. Lunes,Miércoles,Viernes): ").strip()

        try:
            inversion = float(input("Inversión ($): ").strip())
        except ValueError:
            inversion = 150.0

        resultado = registrar_curso(
            codigo=codigo,
            nombre=nombre,
            modalidad=modalidad,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            horario_inicio=hora_inicio,
            horario_fin=hora_fin,
            dias_semana=dias,
            inversion=inversion
        )

        if resultado["exito"]:
            self._data_formatter.mostrar_exito(
                resultado['mensaje'],
                {"Duración": f"{resultado['duracion_semanas']} semanas"}
            )
        else:
            self._data_formatter.mostrar_error(resultado['error'])

    def _listar_cursos(self):
        self._data_formatter.mostrar_encabezado("📋 LISTADO DE CURSOS", 70)
        cursos = listar_cursos()
        self._table_formatter.format_cursos(cursos)

    # -------------------------------------------------------------------------
    # MENÚ INSCRIPCIONES
    # -------------------------------------------------------------------------
    def menu_inscripciones(self):
        """Menú de inscripciones"""
        menu = MenuBuilder.build_enrollments_menu(self)

        while True:
            menu.mostrar()
            opcion = input("\nSeleccione: ").strip()
            if opcion == "0":
                break
            menu.ejecutar(opcion)

    def _inscribir_estudiante(self):
        print("\n📝 INSCRIPCIÓN DE ESTUDIANTE A CURSO")

        try:
            id_est = int(input("ID del Estudiante: ").strip())
            id_cur = int(input("ID del Curso: ").strip())
        except ValueError:
            self._data_formatter.mostrar_error("ID inválido")
            return

        tiene_pdf = input("Tiene PDF de Cédula? (s/n): ").strip().lower() == 's'
        tiene_pago = input("Tiene comprobante de pago? (s/n): ").strip().lower() == 's'

        resultado = inscribir_estudiante(id_est, id_cur, tiene_pdf, tiene_pago)

        if resultado["exito"]:
            self._data_formatter.mostrar_exito(resultado['mensaje'])
        else:
            self._data_formatter.mostrar_error(resultado['error'])
            if "detalles" in resultado:
                for error in resultado["detalles"]:
                    print(f"   - {error}")

    def _validar_requisitos(self):
        print("\n🔍 VALIDAR REQUISITOS DE INSCRIPCIÓN")
        cedula = input("Cédula del Estudiante: ").strip()

        if not validar_cedula_input(cedula):
            self._data_formatter.mostrar_error("Cédula inválida")
            return

        tiene_pdf = input("Tiene PDF de Cédula? (s/n): ").strip().lower() == 's'
        tiene_pago = input("Tiene comprobante de pago? (s/n): ").strip().lower() == 's'
        estado = input("Estado Certificación (aprobado/en_proceso/pendiente): ").strip()

        resultado = validar_inscripcion(cedula, tiene_pdf, tiene_pago, estado)

        if resultado["valida"]:
            print("\n✅ Inscripción VÁLIDA - Puede proceder")
        else:
            print("\n❌ Inscripción INVÁLIDA:")
            for error in resultado["errores"]:
                print(f"   - {error}")

    # -------------------------------------------------------------------------
    # MENÚ CERTIFICADOS
    # -------------------------------------------------------------------------
    def menu_certificados(self):
        """Menú de certificados"""
        menu = MenuBuilder.build_certificates_menu(self)

        while True:
            menu.mostrar()
            opcion = input("\nSeleccione: ").strip()
            if opcion == "0":
                break
            menu.ejecutar(opcion)

    def _generar_certificado(self):
        print("\n📜 GENERAR CERTIFICADO")

        try:
            id_ins = int(input("ID de Inscripción: ").strip())
            calif = float(input("Calificación (0-100): ").strip())
        except ValueError:
            self._data_formatter.mostrar_error("Valores inválidos")
            return

        if calif < 0 or calif > 100:
            self._data_formatter.mostrar_error("La calificación debe estar entre 0 y 100")
            return

        resultado = generar_certificado(id_ins, calif)

        if resultado["exito"]:
            self._data_formatter.mostrar_exito(resultado['mensaje'])
            self._data_formatter.formatear_certificado(resultado)
        else:
            self._data_formatter.mostrar_error(resultado['error'])

    # -------------------------------------------------------------------------
    # MENÚ REPORTES
    # -------------------------------------------------------------------------
    def menu_reportes(self):
        """Menú de reportes"""
        menu = MenuBuilder.build_reports_menu(self)

        while True:
            menu.mostrar()
            opcion = input("\nSeleccione: ").strip()
            if opcion == "0":
                break
            menu.ejecutar(opcion)

    def _reporte_notificaciones(self):
        print("\n📅 REPORTE DE NOTIFICACIONES")
        print("   Política: 30 minutos antes de cada clase")

        # Mostrar ejemplo
        print("\nEjemplo para clase a las 19:00:")
        print(f"   → Notificación se envía a las: {calcular_hora_notificacion('19:00')}")
        print("\nEl sistema generará automáticamente las notificaciones")

    def _reporte_estadisticas(self):
        print("\n📊 ESTADÍSTICAS DEL SISTEMA")
        print("-" * 40)

        est = listar_estudiantes()
        cur = listar_cursos()

        print(f"   Total Estudiantes: {len(est)}")
        print(f"   Total Cursos: {len(cur)}")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

def main():
    """Función principal de la aplicación"""
    print("\n" + "="*50)
    print("  SISTEMA DE GESTIÓN EDUCATIVA ABACOM")
    print("  Instituto de Tecnología y Ciencias")
    print("="*50)
    print("\n  Desarrollado por: Diego Medardo Saavedra García")
    print("  Versión: 1.0.0")
    print("="*50 + "\n")

    app = AplicacionConsola()
    app.iniciar()


if __name__ == "__main__":
    main()