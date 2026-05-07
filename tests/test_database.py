"""Tests para el módulo de persistencia."""

import pytest
import threading
import time
from models.database import (
    DatabaseConnection,
    DatabaseError,
    get_db_connection,
    ejecutar_consulta,
    ejecutar_insert,
    ejecutar_modificacion,
)


class TestSingleton:
    """Tests para el patrón Singleton."""

    def test_misma_instancia_retornada(self):
        """Debe retornar la misma instancia en múltiples llamadas."""
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        assert db1 is db2

    def test_instancia_persistente(self):
        """La instancia debe persistir entre imports."""
        from models import database as db_module
        db1 = db_module.DatabaseConnection()
        db2 = db_module.DatabaseConnection()
        assert db1 is db2


class TestConnection:
    """Tests para la conexión a SQLite."""

    def test_conexion_retornada(self):
        """Debe retornar una conexión válida."""
        db = DatabaseConnection()
        conn = db.get_connection()
        assert conn is not None
        assert conn.execute("SELECT 1").fetchone()[0] == 1

    def test_wal_mode_habilitado(self):
        """WAL mode debe estar habilitado."""
        db = DatabaseConnection()
        conn = db.get_connection()
        mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
        assert mode == "wal"

    def test_foreign_keys_habilitado(self):
        """Foreign keys deben estar habilitados."""
        db = DatabaseConnection()
        conn = db.get_connection()
        fk = conn.execute("PRAGMA foreign_keys").fetchone()[0]
        assert fk == 1


class TestContextManager:
    """Tests para el context manager."""

    def test_transaccion_exitosa(self):
        """Context manager debe manejar transacción correctamente."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            assert dict(result)["test"] == 1

    def test_rollback_en_error(self):
        """Debe hacer rollback cuando ocurre un error."""
        with pytest.raises(DatabaseError):
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tabla_inexistente_xyz")


class TestFunciones:
    """Tests para las funciones helper."""

    def test_ejecutar_consulta(self):
        """ejecutar_consulta debe retornar resultados."""
        results = ejecutar_consulta("SELECT 1 as num UNION SELECT 2")
        assert len(results) == 2
        assert results[0]["num"] == 1

    def test_ejecutar_insert(self):
        """ejecutar_insert debe retornar el ID."""
        db = DatabaseConnection()
        conn = db.get_connection()
        conn.execute("CREATE TABLE IF NOT EXISTS test_insert (id INTEGER PRIMARY KEY, val TEXT)")
        new_id = ejecutar_insert("INSERT INTO test_insert (val) VALUES (?)", ("test_value",))
        assert new_id is not None

    def test_ejecutar_modificacion(self):
        """ejecutar_modificacion debe retornar filas afectadas."""
        db = DatabaseConnection()
        conn = db.get_connection()
        conn.execute("CREATE TABLE IF NOT EXISTS test_update (id INTEGER PRIMARY KEY, val TEXT)")
        ejecutar_insert("INSERT INTO test_update (val) VALUES (?)", ("old",))
        filas = ejecutar_modificacion("UPDATE test_update SET val = ? WHERE val = ?", ("new", "old"))
        assert filas == 1


class TestThreadSafety:
    """Tests para thread-safety."""

    def test_acceso_concurrente(self):
        """Debe manejar acceso concurrente sin errores."""
        errors = []

        def worker():
            try:
                db = DatabaseConnection()
                conn = db.get_connection()
                conn.execute("SELECT 1").fetchone()
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0


class TestReset:
    """Tests para reset de instancia."""

    def test_reset_instancia(self):
        """reset_instance debe permitir reiniciar la instancia."""
        db = DatabaseConnection()
        conn1 = db.get_connection()

        DatabaseConnection.reset_instance()

        db2 = DatabaseConnection()
        conn2 = db2.get_connection()
        assert conn1 is not conn2