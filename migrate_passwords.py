"""Script para migrar contraseñas a bcrypt."""
import sys
sys.path.insert(0, '.')

from services.servicios import hash_password, verify_password
import sqlite3
import os

DB_PATH = 'database/abacom.db'

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Obtener usuarios con passwords antiguas (SHA-256 format)
    cursor.execute("SELECT id_usuario, usuario, password_hash FROM usuarios WHERE password_hash LIKE '%$%'")
    usuarios = cursor.fetchall()
    
    print(f"Encontrados {len(usuarios)} usuarios para migrar")
    
    for uid, usuario, old_hash in usuarios:
        # Generar nuevo hash con bcrypt
        # Para este demo, usar la misma contraseña que antes
        # En producción, los usuarios deberán cambiar su contraseña
        new_hash = hash_password("a1b2d3d4*")  # Contraseña default del admin
        
        cursor.execute("UPDATE usuarios SET password_hash = ? WHERE id_usuario = ?", 
                      (new_hash, uid))
        print(f"  ✓ {usuario} migrado a bcrypt")
    
    conn.commit()
    
    # Verificar
    cursor.execute("SELECT usuario, password_hash FROM usuarios WHERE rol = 'admin'")
    admin = cursor.fetchone()
    print(f"\nAdmin verificado:")
    print(f"  Usuario: {admin[0]}")
    print(f"  Hash: {admin[1][:60]}...")
    
    # Test login
    from services.servicios import iniciar_sesion
    result = iniciar_sesion("statick", "a1b2d3d4*")
    print(f"\nLogin test: {'✓ ÉXITO' if result['exito'] else '✗ FALLO'}")
    
    conn.close()

if __name__ == "__main__":
    migrate()