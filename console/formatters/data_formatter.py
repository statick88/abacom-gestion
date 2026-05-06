"""Data formatting utilities for console display."""


class DataFormatter:
    """Format various data types for display"""

    @staticmethod
    def mostrar_estudiante(estudiante: dict) -> None:
        """Display student details"""
        print("\n✅ ESTUDIANTE ENCONTRADO:")
        print(f"   ID: {estudiante['id_estudiante']}")
        print(f"   Nombres: {estudiante['nombres_completos']}")
        print(f"   Cédula: {estudiante['identificacion']}")
        print(f"   Celular: {estudiante['celular']}")
        print(f"   Correo: {estudiante['correo_electronico']}")

    @staticmethod
    def mostrar_error(mensaje: str) -> None:
        """Display error message"""
        print(f"\n❌ {mensaje}")

    @staticmethod
    def mostrar_exito(mensaje: str, detalles: dict = None) -> None:
        """Display success message with optional details"""
        print(f"\n✅ {mensaje}")
        if detalles:
            for key, value in detalles.items():
                print(f"   {key}: {value}")

    @staticmethod
    def mostrar_encabezado(titulo: str, longitud: int = 40) -> None:
        """Display section header"""
        print(f"\n{titulo}")
        print("-" * longitud)

    @staticmethod
    def formatear_certificado(resultado: dict) -> None:
        """Format and display certificate result"""
        print(f"\n   Certificado: {resultado['numero_certificado']}")
        print(f"   Estado: {resultado['estado']}")
        if resultado.get('aval_ministerio'):
            print(f"   Aval: {resultado['aval_ministerio']}")