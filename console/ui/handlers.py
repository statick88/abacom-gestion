"""Menu builders for console application."""

from .menu import MenuConsola


class MenuBuilder:
    """Builder for creating application menus"""

    @staticmethod
    def build_main_menu(app) -> MenuConsola:
        """Build the main application menu"""
        menu = MenuConsola()
        menu.titulo = "SISTEMA DE GESTIÓN ABACOM"
        menu.agregar_opcion("1", "Gestionar Estudiantes", app.menu_estudiantes)
        menu.agregar_opcion("2", "Gestionar Cursos", app.menu_cursos)
        menu.agregar_opcion("3", "Gestionar Inscripciones", app.menu_inscripciones)
        menu.agregar_opcion("4", "Generar Certificados", app.menu_certificados)
        menu.agregar_opcion("5", "Reportes", app.menu_reportes)
        return menu

    @staticmethod
    def build_students_menu(app) -> MenuConsola:
        """Build students management menu"""
        menu = MenuConsola()
        menu.titulo = "GESTIÓN DE ESTUDIANTES"
        menu.agregar_opcion("1", "Registrar Estudiante", app._registrar_estudiante)
        menu.agregar_opcion("2", "Buscar por Cédula", app._buscar_estudiante)
        menu.agregar_opcion("3", "Listar Estudiantes", app._listar_estudiantes)
        return menu

    @staticmethod
    def build_courses_menu(app) -> MenuConsola:
        """Build courses management menu"""
        menu = MenuConsola()
        menu.titulo = "GESTIÓN DE CURSOS"
        menu.agregar_opcion("1", "Registrar Curso", app._registrar_curso)
        menu.agregar_opcion("2", "Listar Cursos", app._listar_cursos)
        return menu

    @staticmethod
    def build_enrollments_menu(app) -> MenuConsola:
        """Build enrollments menu"""
        menu = MenuConsola()
        menu.titulo = "INSCRIPCIONES"
        menu.agregar_opcion("1", "Inscribir Estudiante", app._inscribir_estudiante)
        menu.agregar_opcion("2", "Validar Requisitos", app._validar_requisitos)
        return menu

    @staticmethod
    def build_certificates_menu(app) -> MenuConsola:
        """Build certificates menu"""
        menu = MenuConsola()
        menu.titulo = "CERTIFICACIONES"
        menu.agregar_opcion("1", "Generar Certificado", app._generar_certificado)
        return menu

    @staticmethod
    def build_reports_menu(app) -> MenuConsola:
        """Build reports menu"""
        menu = MenuConsola()
        menu.titulo = "REPORTES"
        menu.agregar_opcion("1", "Ver Notificaciones (30 min antes)", app._reporte_notificaciones)
        menu.agregar_opcion("2", "Estadísticas del Sistema", app._reporte_estadisticas)
        return menu