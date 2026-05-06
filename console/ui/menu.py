"""Menu management for console application."""


class MenuConsola:
    """Gestor de menús para la aplicación de consola"""

    def __init__(self):
        self.opciones = {}
        self.titulo = ""

    def agregar_opcion(self, numero: str, texto: str, funcion):
        """Add an option to the menu"""
        self.opciones[numero] = {"texto": texto, "funcion": funcion}

    def mostrar(self):
        """Display the menu"""
        from console.formatters.menu_formatter import MenuFormatter
        MenuFormatter().mostrar_menu(self.titulo, self.opciones)

    def ejecutar(self, opcion: str) -> bool:
        """Execute the selected option"""
        if opcion in self.opciones:
            self.opciones[opcion]["funcion"]()
            return False
        elif opcion == "0":
            return True
        else:
            print("\n❌ Opción inválida")
            return False