"""
================================================================================
MÓDULO DE CONEXIÓN A BASE DE DATOS
================================================================================
Sistema de Gestión Educativa ABACOM
Conexión a SQLite3

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

# Importar configuración
try:
    from config import DB_PATH
except ImportError:
    # Fallback si no se puede importar
    DB_PATH = "abacom-gestion/database/abacom.db"


class DatabaseError(Exception):
    """Excepción personalizada para errores de base de datos"""
    pass


class DatabaseConnection:
    """
    Gestor de conexión a la base de datos SQLite3.
    Implementa el patrón Singleton para una única conexión.
    """

    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[sqlite3.Connection] = None
    _db_path: str = ""

    def __new__(cls, db_path: str = DB_PATH):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._db_path = db_path
        return cls._instance

    def __init__(self, db_path: str = DB_PATH):
        """Inicializa la conexión a la base de datos"""
        self._db_path = db_path

    def connect(self) -> sqlite3.Connection:
        """
        Establece conexión a la base de datos.
        Returns:
            sqlite3.Connection: Objeto de conexión
        Raises:
            DatabaseError: Si no puede conectar
        """
        try:
            # Asegurar que el directorio existe
            db_file = Path(self._db_path)
            db_file.parent.mkdir(parents=True, exist_ok=True)

            self._connection = sqlite3.connect(self._db_path)
            self._connection.row_factory = sqlite3.Row  # Para acceso por nombre de columna
            return self._connection
        except sqlite3.Error as e:
            raise DatabaseError(f"Error al conectar a la base de datos: {e}")

    def disconnect(self):
        """Cierra la conexión a la base de datos"""
        if self._connection:
            self._connection.close()
            self._connection = None

    def get_connection(self) -> sqlite3.Connection:
        """
        Obtiene la conexión activa o crea una nueva.
        Returns:
            sqlite3.Connection
        """
        if self._connection is None:
            return self.connect()
        return self._connection


@contextmanager
def get_db_connection(db_path: str = DB_PATH):
    """
    Administrador de contexto para manejar conexiones a la base de datos.
    Uso:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estudiantes")
    
    Args:
        db_path: Ruta al archivo de base de datos SQLite
    
    Yields:
        sqlite3.Connection
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise DatabaseError(f"Error en la base de datos: {e}")
    finally:
        if conn:
            conn.close()


# =============================================================================
# FUNCIONES DE CONSULTA - ESTILO FUNCIONAL
# =============================================================================

def ejecutar_consulta(query: str, params: tuple = (), db_path: str = DB_PATH) -> list:
    """
    Ejecuta una consulta SELECT y retorna los resultados.
    
    Args:
        query: Sentencia SQL SELECT
        params: Tupla con parámetros para la consulta
        db_path: Ruta a la base de datos
    
    Returns:
        list: Lista de filas (cada fila es un diccionario con nombres de columna)
    """
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        return [dict(fila) for fila in resultados]


def ejecutar_modificacion(query: str, params: tuple = (), db_path: str = DB_PATH) -> int:
    """
    Ejecuta una consulta INSERT, UPDATE o DELETE.
    
    Args:
        query: Sentencia SQL de modificación
        params: Tupla con parámetros
        db_path: Ruta a la base de datos
    
    Returns:
        int: Número de filas afectadas
    """
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.lastrowid if cursor.lastrowid else cursor.rowcount


def obtener_por_id(tabla: str, id: int, db_path: str = DB_PATH) -> Optional[dict]:
    """
    Obtiene un registro por su ID.
    
    Args:
        tabla: Nombre de la tabla
        id: ID del registro
        db_path: Ruta a la base de datos
    
    Returns:
        Optional[dict]: Registro encontrado o None
    """
    query = f"SELECT * FROM {tabla} WHERE id_{tabla[:-1]} = ?"
    resultados = ejecutar_consulta(query, (id,), db_path)
    return resultados[0] if resultados else None


# =============================================================================
# PRUEBAS DE CONEXIÓN
# =============================================================================

if __name__ == "__main__":
    # Prueba de conexión
    print("=== Prueba de Conexión a Base de Datos ABACOM ===\n")

    # Probar conexión directa
    db = DatabaseConnection("abacom.db")
    conn = db.connect()
    print(f"✓ Conexión establecida: {db._db_path}")

    # Ver tablas existentes
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()
    print(f"✓ Tablas en la base de datos: {len(tablas)}")
    for tabla in tablas:
        print(f"  - {tabla[0]}")

    # Contar registros
    for tabla in tablas:
        if tabla[0] != 'sqlite_sequence':
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla[0]}")
                count = cursor.fetchone()[0]
                print(f"  → {tabla[0]}: {count} registros")
            except:
                pass

    db.disconnect()
    print("\n✓ Prueba de conexión completada exitosamente")