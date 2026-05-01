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
from datetime import datetime

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


class MenuConsola:
    """Gestor de menús para la aplicación de consola"""

    def __init__(self):
        self.opciones = {}
        self.titulo = ""

    def agregar_opcion(self, numero: str, texto: str, funcion):
        self.opciones[numero] = {"texto": texto, "funcion": funcion}

    def mostrar(self):
        print(f"\n{'='*50}")
        print(f"  {self.titulo}")
        print('='*50)
        for num, op in self.opciones.items():
            print(f"  {num}. {op['texto']}")
        print("  0. Volver al menú principal")
        print('='*50)

    def ejecutar(self, opcion: str):
        if opcion in self.opciones:
            return self.opciones[opcion]["funcion"]()
        elif opcion == "0":
            return True
        else:
            print("\n❌ Opción inválida")
            return False


class AplicacionConsola:
    """Aplicación principal de consola"""

    def __init__(self):
        self.db_path = DB_PATH
        self.menus = {}
        self.menu_principal = None

    def iniciar(self):
        """Inicia la aplicación"""
        self._construir_menus()
        self._ejecutar_menu_principal()

    def _construir_menus(self):
        """Construye los menús de la aplicación"""

        # Menú Principal
        self.menu_principal = MenuConsola()
        self.menu_principal.titulo = "SISTEMA DE GESTIÓN ABACOM"
        self.menu_principal.agregar_opcion("1", "Gestionar Estudiantes", self.menu_estudiantes)
        self.menu_principal.agregar_opcion("2", "Gestionar Cursos", self.menu_cursos)
        self.menu_principal.agregar_opcion("3", "Gestionar Inscripciones", self.menu_inscripciones)
        self.menu_principal.agregar_opcion("4", "Generar Certificados", self.menu_certificados)
        self.menu_principal.agregar_opcion("5", "Reportes", self.menu_reportes)

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
        menu = MenuConsola()
        menu.titulo = "GESTIÓN DE ESTUDIANTES"
        menu.agregar_opcion("1", "Registrar Estudiante", self._registrar_estudiante)
        menu.agregar_opcion("2", "Buscar por Cédula", self._buscar_estudiante)
        menu.agregar_opcion("3", "Listar Estudiantes", self._listar_estudiantes)

        while True:
            menu.mostrar()
            opcion = input("\nSeleccione: ").strip()
            if opcion == "0":
                break
            menu.ejecutar(opcion)

    def _registrar_estudiante(self):
        print("\n📝 REGISTRO DE ESTUDIANTE")
        print("-" * 40)

        # Validar cédula primero
        cedula = input("Cédula de Identidad (10 dígitos): ").strip()
        if not validar_cedula_ecuador(cedula):
            print("\n❌ Cédula inválida. Debe tener 10 dígitos.")
            return

        nombres = input("Nombres Completos: ").strip()
        if not nombres:
            print("\n❌ Error: Nombres son requeridos")
            return

        telefono = input("Teléfono Fijo (opcional): ").strip()
        celular = input("Celular: ").strip()
        if not celular:
            print("\n❌ Error: Celular es requerido")
            return

        correo = input("Correo Electrónico: ").strip()
        if not correo:
            print("\n❌ Error: Correo es requerido")
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
            print(f"\n✅ {resultado['mensaje']}")
            print(f"   ID Estudiante: {resultado['id_estudiante']}")
        else:
            print(f"\n❌ {resultado['error']}")

    def _buscar_estudiante(self):
        print("\n🔍 BUSCAR ESTUDIANTE POR CÉDULA")
        cedula = input("Ingrese la cédula: ").strip()

        if not validar_cedula_ecuador(cedula):
            print("\n❌ Formato de cédula inválido")
            return

        estudiante = obtener_estudiante_por_cedula(cedula)

        if estudiante:
            print("\n✅ ESTUDIANTE ENCONTRADO:")
            print(f"   ID: {estudiante['id_estudiante']}")
            print(f"   Nombres: {estudiante['nombres_completos']}")
            print(f"   Cédula: {estudiante['identificacion']}")
            print(f"   Celular: {estudiante['celular']}")
            print(f"   Correo: {estudiante['correo_electronico']}")
        else:
            print("\n❌ Estudiante no encontrado")

    def _listar_estudiantes(self):
        print("\n📋 LISTADO DE ESTUDIANTES")
        print("-" * 60)

        estudiantes = listar_estudiantes()

        if not estudiantes:
            print("No hay estudiantes registrados")
            return

        print(f"{'ID':<4} | {'Nombres':<25} | {'Cédula':<12} | {'Celular':<12}")
        print("-" * 60)

        for e in estudiantes:
            print(f"{e['id_estudiante']:<4} | {e['nombres_completos'][:25]:<25} | "
                  f"{e['identificacion']:<12} | {e['celular']:<12}")

    # -------------------------------------------------------------------------
    # MENÚ CURSOS
    # -------------------------------------------------------------------------
    def menu_cursos(self):
        """Menú de gestión de cursos"""
        menu = MenuConsola()
        menu.titulo = "GESTIÓN DE CURSOS"
        menu.agregar_opcion("1", "Registrar Curso", self._registrar_curso)
        menu.agregar_opcion("2", "Listar Cursos", self._listar_cursos)

        while True:
            menu.mostrar()
            opcion = input("\nSeleccione: ").strip()
            if opcion == "0":
                break
            menu.ejecutar(opcion)

    def _registrar_curso(self):
        print("\n📝 REGISTRO DE CURSO")
        print("-" * 40)

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
            print(f"\n✅ {resultado['mensaje']}")
            print(f"   Duración: {resultado['duracion_semanas']} semanas")
        else:
            print(f"\n❌ {resultado['error']}")

    def _listar_cursos(self):
        print("\n📋 LISTADO DE CURSOS")
        print("-" * 70)

        cursos = listar_cursos()

        if not cursos:
            print("No hay cursos registrados")
            return

        print(f"{'Código':<6} | {'Nombre':<25} | {'Inicio':<12} | {'Estado':<10}")
        print("-" * 70)

        for c in cursos:
            print(f"{c['codigo']:<6} | {c['nombre'][:25]:<25} | "
                  f"{c['fecha_inicio']:<12} | {c['estado']:<10}")

    # -------------------------------------------------------------------------
    # MENÚ INSCRIPCIONES
    # -------------------------------------------------------------------------
    def menu_inscripciones(self):
        """Menú de inscripciones"""
        menu = MenuConsola()
        menu.titulo = "INSCRIPCIONES"
        menu.agregar_opcion("1", "Inscribir Estudiante", self._inscribir_estudiante)
        menu.agregar_opcion("2", "Validar Requisitos", self._validar_requisitos)

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
            print("\n❌ ID inválido")
            return

        tiene_pdf = input("Tiene PDF de Cédula? (s/n): ").strip().lower() == 's'
        tiene_pago = input("Tiene comprobante de pago? (s/n): ").strip().lower() == 's'

        resultado = inscribir_estudiante(id_est, id_cur, tiene_pdf, tiene_pago)

        if resultado["exito"]:
            print(f"\n✅ {resultado['mensaje']}")
        else:
            print(f"\n❌ {resultado['error']}")
            if "detalles" in resultado:
                for error in resultado["detalles"]:
                    print(f"   - {error}")

    def _validar_requisitos(self):
        print("\n🔍 VALIDAR REQUISITOS DE INSCRIPCIÓN")
        cedula = input("Cédula del Estudiante: ").strip()

        if not validar_cedula_ecuador(cedula):
            print("\n❌ Cédula inválida")
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
        menu = MenuConsola()
        menu.titulo = "CERTIFICACIONES"
        menu.agregar_opcion("1", "Generar Certificado", self._generar_certificado)

        while True:
            menu.mostrar()
            opcion = input("\nSeleccione: ").strip()
            if opcion == "0":
                break
            menu.ejecutar(opcion)

    def _generar_certulario(self):
        print("\n📜 GENERAR CERTIFICADO")

        try:
            id_ins = int(input("ID de Inscripción: ").strip())
            calif = float(input("Calificación (0-100): ").strip())
        except ValueError:
            print("\n❌ Valores inválidos")
            return

        if calif < 0 or calif > 100:
            print("\n❌ La calificación debe estar entre 0 y 100")
            return

        resultado = generar_certificado(id_ins, calif)

        if resultado["exito"]:
            print(f"\n✅ {resultado['mensaje']}")
            print(f"\n   Certificado: {resultado['numero_certificado']}")
            print(f"   Estado: {resultado['estado']}")
            if resultado['aval_ministerio']:
                print(f"   Aval: {resultado['aval_ministerio']}")
        else:
            print(f"\n❌ {resultado['error']}")

    def _generar_certificado(self):
        print("\n📜 GENERAR CERTIFICADO")

        try:
            id_ins = int(input("ID de Inscripción: ").strip())
            calif = float(input("Calificación (0-100): ").strip())
        except ValueError:
            print("\n❌ Valores inválidos")
            return

        if calif < 0 or calif > 100:
            print("\n❌ La calificación debe estar entre 0 y 100")
            return

        resultado = generar_certificado(id_ins, calif)

        if resultado["exito"]:
            print(f"\n✅ {resultado['mensaje']}")
            print(f"\n   Certificado: {resultado['numero_certificado']}")
            print(f"   Estado: {resultado['estado']}")
            if resultado['aval_ministerio']:
                print(f"   Aval: {resultado['aval_ministerio']}")
        else:
            print(f"\n❌ {resultado['error']}")

    # -------------------------------------------------------------------------
    # MENÚ REPORTES
    # -------------------------------------------------------------------------
    def menu_reportes(self):
        """Menú de reportes"""
        menu = MenuConsola()
        menu.titulo = "REPORTES"
        menu.agregar_opcion("1", "Ver Notificaciones (30 min antes)", self._reporte_notificaciones)
        menu.agregar_opcion("2", "Estadísticas del Sistema", self._reporte_estadisticas)

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