"""
================================================================================
MIGRACIÓN: Crear tabla usuarios
================================================================================
Autor: Diego Medardo Saavedra García
Instituto: ABACOM
Fecha: 2026-04-30
================================================================================
"""

import sqlite3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DB_PATH

def crear_tabla_usuarios():
    """Crea la tabla usuarios si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            nombres TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'estudiante',
            estado TEXT NOT NULL DEFAULT 'activo',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    
    conn.commit()
    
    # Verificar si se creó
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
    if cursor.fetchone():
        print("✓ Tabla 'usuarios' creada exitosamente")
    else:
        print("✗ Error al crear tabla 'usuarios'")
    
    conn.close()

if __name__ == "__main__":
    crear_tabla_usuarios()