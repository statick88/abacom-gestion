"""
================================================================================
PUNTO DE ENTRADA PRINCIPAL - SISTEMA DE GESTIÓN ABACOM
================================================================================
Permite ejecutar la aplicación en diferentes modos.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

import sys
import os

# Agregar el directorio raíz al path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)


def main():
    """Función principal con menú de selección de interfaz."""
    
    print("\n" + "=" * 60)
    print("  🎓 SISTEMA DE GESTIÓN EDUCATIVA ABACOM")
    print("  Instituto de Tecnología y Ciencias")
    print("=" * 60)
    print("\n  Seleccione la interfaz:")
    print("\n  1. 💻 Interfaz de Consola (CLI)")
    print("  2. 🖥️ Interfaz Gráfica (PyQt5)")
    print("  3. 🌐 Interfaz Web (Flask) - Requiere instalación")
    print("  4. 🧪 Ejecutar Tests")
    print("  5. 📦 Generar Datos de Prueba")
    print("  0. ❌ Salir")
    print("=" * 60)
    
    opcion = input("\nSeleccione una opción: ").strip()
    
    if opcion == "1":
        # Consola
        print("\n🚀 Iniciando interfaz de consola...")
        from console.app import main as console_main
        console_main()
        
    elif opcion == "2":
        # GUI - tkinter (built-in, no requiere instalación)
        print("\n🚀 Iniciando interfaz gráfica (tkinter)...")
        try:
            from gui.app import main as gui_main
            gui_main()
        except Exception as e:
            print(f"\n❌ Error al iniciar GUI: {e}")
            print("   Asegúrese de tener python-tk instalado (brew install python-tk)")
            import traceback
            traceback.print_exc()
            
    elif opcion == "3":
        # Web
        print("\n🚀 Iniciando interfaz web...")
        try:
            from web.app import app
            print("\n🌐 Servidor iniciado en: http://localhost:5000")
            print("   Presione Ctrl+C para detener\n")
            app.run(debug=True, host='0.0.0.0', port=5000)
        except ImportError:
            print("\n❌ Error: Flask no está instalado.")
            print("   Instale con: pip install flask flask-cors")
            
    elif opcion == "4":
        # Tests
        print("\n🧪 Ejecutando pruebas...")
        os.system(f"cd {PROJECT_DIR} && python3 -m pytest specs/ -v")
        print("\n✅ Pruebas completadas")
        
    elif opcion == "5":
        # Datos de prueba
        print("\n📦 Generando datos de prueba...")
        from test_e2e import main as test_main
        test_main()
        
    elif opcion == "0":
        print("\n👋 Gracias por usar el Sistema ABACOM")
        print("   Hasta luego.\n")
        
    else:
        print("\n❌ Opción inválida")


if __name__ == "__main__":
    main()