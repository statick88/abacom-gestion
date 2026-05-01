"""Script para crear tabla de usuarios y usuario admin."""
import sqlite3
import hashlib
import secrets

DB_PATH = 'database/abacom.db'

def hash_password(password):
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((salt + password).encode())
    return f'{salt}${hash_obj.hexdigest()}'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Crear tabla usuarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    nombres TEXT NOT NULL,
    rol TEXT DEFAULT 'estudiante' CHECK(rol IN ('admin', 'docente', 'estudiante')),
    estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'inactivo', 'suspendido')),
    ultimo_login TIMESTAMP,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(usuario),
    UNIQUE(email)
)
''')
print('Tabla usuarios creada')

# Insertar usuario admin
password_hash = hash_password('a1b2d3d4*')
cursor.execute('''INSERT OR IGNORE INTO usuarios (usuario, email, password_hash, nombres, rol, estado)
                  VALUES (?, ?, ?, ?, ?, ?)''',
               ('statick', 'dsaavedra88@gmail.com', password_hash,
                'Diego Medardo Saavedra García', 'admin', 'activo'))
conn.commit()
print('Usuario admin creado')

# Verificar
cursor.execute('SELECT usuario, email, nombres, rol FROM usuarios')
print('Usuarios en BD:', cursor.fetchall())

conn.close()
print('Listo!')