"""Menu display formatting utilities."""


class MenuFormatter:
    """Format menus for console display"""

    def mostrar_menu(self, titulo: str, opciones: dict) -> None:
        """Display a formatted menu"""
        print(f"\n{'='*50}")
        print(f"  {titulo}")
        print('='*50)
        for num, op in opciones.items():
            print(f"  {num}. {op['texto']}")
        print("  0. Volver al menú principal")
        print('='*50)