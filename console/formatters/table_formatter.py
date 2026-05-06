"""Table formatting utilities for console display."""


class TableFormatter:
    """Format data as tables for console output"""

    @staticmethod
    def format_estudiantes(estudiantes: list) -> None:
        """Format and display students list as table"""
        if not estudiantes:
            print("No hay estudiantes registrados")
            return

        print(f"{'ID':<4} | {'Nombres':<25} | {'Cédula':<12} | {'Celular':<12}")
        print("-" * 60)

        for e in estudiantes:
            print(f"{e['id_estudiante']:<4} | {e['nombres_completos'][:25]:<25} | "
                  f"{e['identificacion']:<12} | {e['celular']:<12}")

    @staticmethod
    def format_cursos(cursos: list) -> None:
        """Format and display courses list as table"""
        if not cursos:
            print("No hay cursos registrados")
            return

        print(f"{'Código':<6} | {'Nombre':<25} | {'Inicio':<12} | {'Estado':<10}")
        print("-" * 70)

        for c in cursos:
            print(f"{c['codigo']:<6} | {c['nombre'][:25]:<25} | "
                  f"{c['fecha_inicio']:<12} | {c['estado']:<10}")