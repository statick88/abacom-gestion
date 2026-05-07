"""
================================================================================
MÓDULO DE CONEXIÓN A BASE DE DATOS
================================================================================
Sistema de Gestión Educativa ABACOM
Conexión a SQLite3 con patrón Singleton y context managers.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

import sqlite3
import threading
from pathlib import Path
from typing import Optional, List, Tuple, Any, Dict
from contextlib import contextmanager

try:
    from config import DB_PATH
except ImportError:
    DB_PATH = "abacom-gestion/database/abacom.db"


class DatabaseError(Exception):
    """Excepción personalizada para errores de base de datos."""

    def __init__(self, message: str, original: Optional[Exception] = None):
        self.message = message
        self.original = original
        super().__init__(self.message)


class DatabaseConnection:
    """
    Gestor de conexión a la base de datos SQLite3.

    Implementa el patrón Singleton para garantizar una única instancia
    de conexión en toda la aplicación.
    """

    _instance: Optional["DatabaseConnection"] = None
    _lock: threading.Lock = threading.Lock()
    _db_path: str = ""

    def __new__(cls, db_path: str = DB_PATH) -> "DatabaseConnection":
        """Implementa el patrón Singleton con thread-safety."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
                    cls._db_path = db_path
        return cls._instance

    def __init__(self, db_path: str = DB_PATH) -> None:
        """Inicializa la conexión a la base de datos."""
        if self._initialized:
            return
        self._initialized = True
        self._connection: Optional[sqlite3.Connection] = None
        self._db_path = db_path
        self._conn_lock = threading.Lock()

    def connect(self) -> sqlite3.Connection:
        """Establece conexión a la base de datos."""
        with self._conn_lock:
            if self._connection is not None:
                return self._connection

            try:
                db_dir = Path(self._db_path).parent
                db_dir.mkdir(parents=True, exist_ok=True)

                self._connection = sqlite3.connect(
                    self._db_path,
                    check_same_thread=False
                )
                self._connection.row_factory = sqlite3.Row
                self._connection.execute("PRAGMA foreign_keys = ON")
                self._connection.execute("PRAGMA journal_mode=WAL")
                self._connection.execute("PRAGMA synchronous=NORMAL")

                return self._connection

            except sqlite3.Error as e:
                raise DatabaseError(f"Error al conectar a la base de datos: {e}", e)

    def close(self) -> None:
        """Cierra la conexión a la base de datos."""
        with self._conn_lock:
            if self._connection:
                self._connection.close()
                self._connection = None

    def get_connection(self) -> sqlite3.Connection:
        """Obtiene la conexión actual o crea una nueva."""
        if self._connection is None:
            return self.connect()
        return self._connection

    @classmethod
    def reset_instance(cls) -> None:
        """Resetea la instancia (para testing)."""
        with cls._lock:
            if cls._instance:
                cls._instance.close()
                cls._instance = None


@contextmanager
def get_db_connection(db_path: str = DB_PATH):
    """
    Context manager para manejar transacciones en la base de datos.

    No cierra la conexión del Singleton, solo administra la transacción.

    Args:
        db_path: Ruta al archivo de base de datos.

    Yields:
        sqlite3.Connection: Conexión activa a la base de datos.

    Raises:
        DatabaseError: Si ocurre un error de base de datos.
    """
    db = DatabaseConnection(db_path)
    conn = db.get_connection()
    try:
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise DatabaseError(f"Error en la base de datos: {e}", e)


def ejecutar_consulta(
    query: str,
    params: Tuple[Any, ...] = (),
    db_path: str = DB_PATH,
) -> List[Dict[str, Any]]:
    """
    Ejecuta una consulta SELECT y retorna los resultados.

    Args:
        query: Consulta SQL con parámetros opcionales (?).
        params: Tupla con los valores para los parámetros.
        db_path: Ruta a la base de datos.

    Returns:
        List[Dict]: Lista de diccionarios con los resultados.

    Raises:
        DatabaseError: Si la consulta falla.
    """
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    except sqlite3.Error as e:
        raise DatabaseError(f"Error en la consulta: {e}", e)


def ejecutar_modificacion(
    query: str,
    params: Tuple[Any, ...] = (),
    db_path: str = DB_PATH,
) -> int:
    """
    Ejecuta una operación INSERT, UPDATE o DELETE.

    Args:
        query: Consulta SQL de modificación.
        params: Tupla con los valores para los parámetros.
        db_path: Ruta a la base de datos.

    Returns:
        int: Número de filas afectadas.

    Raises:
        DatabaseError: Si la operación falla.
    """
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount

    except sqlite3.Error as e:
        raise DatabaseError(f"Error en la modificación: {e}", e)


def ejecutar_insert(
    query: str,
    params: Tuple[Any, ...] = (),
    db_path: str = DB_PATH,
) -> int:
    """
    Ejecuta un INSERT y retorna el ID del registro insertado.

    Args:
        query: Consulta SQL INSERT.
        params: Tupla con los valores para los parámetros.
        db_path: Ruta a la base de datos.

    Returns:
        int: ID del nuevo registro insertado.

    Raises:
        DatabaseError: Si la inserción falla.
    """
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.lastrowid

    except sqlite3.Error as e:
        raise DatabaseError(f"Error en la inserción: {e}", e)


def ejecutar_varias(
    queries: List[Tuple[str, Tuple[Any, ...]]],
    db_path: str = DB_PATH,
) -> None:
    """
    Ejecuta múltiples consultas en una transacción.

    Args:
        queries: Lista de tuplas (query, params).
        db_path: Ruta a la base de datos.

    Raises:
        DatabaseError: Si alguna consulta falla.
    """
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            for query, params in queries:
                cursor.execute(query, params)

    except sqlite3.Error as e:
        raise DatabaseError(f"Error en ejecución múltiple: {e}", e)