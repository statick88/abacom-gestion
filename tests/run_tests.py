"""Run database tests manually."""

import sys
sys.path.insert(0, '.')

from models.database import (
    DatabaseConnection,
    DatabaseError,
    get_db_connection,
    ejecutar_consulta,
    ejecutar_insert,
    ejecutar_modificacion,
)
import threading


def test_singleton():
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    assert db1 is db2, "FAILED: singleton"
    print("[PASS] test_singleton")


def test_conexion():
    db = DatabaseConnection()
    conn = db.get_connection()
    assert conn is not None, "FAILED: connection"
    print("[PASS] test_conexion")


def test_wal_mode():
    db = DatabaseConnection()
    conn = db.get_connection()
    mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
    assert mode == "wal", "FAILED: wal mode"
    print("[PASS] test_wal_mode")


def test_foreign_keys():
    db = DatabaseConnection()
    conn = db.get_connection()
    fk = conn.execute("PRAGMA foreign_keys").fetchone()[0]
    assert fk == 1, "FAILED: fk"
    print("[PASS] test_foreign_keys")


def test_context_manager():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        assert dict(result)["test"] == 1, "FAILED: context manager"
    print("[PASS] test_context_manager")


def test_ejecutar_consulta():
    results = ejecutar_consulta("SELECT 1 as num UNION SELECT 2")
    assert len(results) == 2, "FAILED: consulta rows"
    assert results[0]["num"] == 1, "FAILED: consulta value"
    print("[PASS] test_ejecutar_consulta")


def test_ejecutar_insert():
    db = DatabaseConnection()
    conn = db.get_connection()
    conn.execute("CREATE TABLE IF NOT EXISTS test_insert (id INTEGER PRIMARY KEY, val TEXT)")
    new_id = ejecutar_insert("INSERT INTO test_insert (val) VALUES (?)", ("test_value",))
    assert new_id is not None, "FAILED: insert id"
    print("[PASS] test_ejecutar_insert")


def test_ejecutar_modificacion():
    db = DatabaseConnection()
    conn = db.get_connection()
    conn.execute("CREATE TABLE IF NOT EXISTS test_update (id INTEGER PRIMARY KEY, val TEXT)")
    ejecutar_insert("INSERT INTO test_update (val) VALUES (?)", ("old",))
    filas = ejecutar_modificacion("UPDATE test_update SET val = ? WHERE val = ?", ("new", "old"))
    assert filas == 1, "FAILED: modificacion"
    print("[PASS] test_ejecutar_modificacion")


def test_thread_safety():
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

    assert len(errors) == 0, "FAILED: thread errors"
    print("[PASS] test_thread_safety")


def test_reset():
    db = DatabaseConnection()
    conn1 = db.get_connection()
    DatabaseConnection.reset_instance()
    db2 = DatabaseConnection()
    conn2 = db2.get_connection()
    assert conn1 is not conn2, "FAILED: reset"
    print("[PASS] test_reset")


if __name__ == "__main__":
    tests = [
        test_singleton,
        test_conexion,
        test_wal_mode,
        test_foreign_keys,
        test_context_manager,
        test_ejecutar_consulta,
        test_ejecutar_insert,
        test_ejecutar_modificacion,
        test_thread_safety,
        test_reset,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"[FAIL] {test.__name__}: {e}")
            failed += 1

    print(f"\n{'='*40}")
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")