# Manual del Programador - ABACOM Gestión

## 1. Arquitectura del Sistema

```
abacom-gestion/
├── gui/              # Interfaz gráfica (tkinter)
├── services/         # Lógica de negocio
├── models/           # Modelos de datos
├── database/         # Schema y conexión SQLite
├── config/           # Configuración
├── assets/           # Recursos estáticos
├── logs/             # Logs de auditoría
├── tests/            # Pruebas automatizadas
└── build/            # Scripts de build
```

## 2. Tecnologías

| Componente | Tecnología |
|------------|------------|
| GUI | tkinter (Python stdlib) |
| Base de datos | SQLite3 |
| Hashing | bcrypt (rounds=12) |
| Testing | pytest |
| Build | PyInstaller |

## 3. Configuración

### Variables de Entorno
```bash
# Obligatorio: Credenciales admin
export ABACOM_ADMIN_USER="statick"
export ABACOM_ADMIN_PASSWORD="<password>"
export ABACOM_ADMIN_EMAIL="<email>"

# Opcional
export DB_PATH="database/abacom.db"
export LOG_LEVEL="INFO"
```

### Config YAML (config/config.yaml)
```yaml
database:
  path: "database/abacom.db"
  
security:
  max_login_attempts: 5
  lockout_minutes: 5
  bcrypt_rounds: 12
```

## 4. Estructura de la Base de Datos

### Tablas Principales
- **usuarios**: Autenticación (usuario, email, password_hash, rol, estado)
- **estudiantes**: Datos de estudiantes (identificacion, nombres, contacto)
- **docentes**: Datos de docentes
- **cursos**: Información de cursos (codigo, nombre, horario, costo, estado)
- **inscripciones**: Matriculaciones (estudiante, curso, estado, pagos)
- **certificados**: Certificaciones (inscripcion, nota, fecha)
- **auditoria**: Log de acciones (usuario, accion, detalles, timestamp)

## 5. Servicios (API)

### Autenticación
```python
from services.servicios import iniciar_sesion, registrar_usuario

# Login
result = iniciar_sesion("usuario", "password")
# Returns: {"exito": bool, "mensaje": str, "usuario_data": dict}

# Registro
result = registrar_usuario("user", "email", "pass", "nombre", "rol")
```

### Gestión de Entidades
```python
# Estudiantes
from services.servicios import (
    registrar_estudiante, listar_estudiantes,
    actualizar_estudiante, eliminar_estudiante
)

# Cursos
from services.servicios import (
    registrar_curso, listar_cursos,
    actualizar_curso, eliminar_curso
)

# Inscripciones
from services.servicios import (
    inscribir_estudiante, listar_inscripciones,
    actualizar_inscripcion
)

# Certificados
from services.servicios import (
    generar_certificado, listar_certificaciones,
    validar_certificado
)
```

## 6. Construcción de Ejecutables

### Requisitos
```bash
pip install pyinstaller pillow pyyaml bcrypt cryptography
```

### Build para macOS
```bash
make macos
# Output: dist/macos/ABACOM_Gestion.app
```

### Build para Windows
```bash
make windows
# Output: dist/windows/ABACOM_Gestion/
```

### Build para Linux
```bash
make linux
# Output: dist/linux/ABACOM_Gestion/
```

## 7. Testing

### Ejecutar todas las pruebas
```bash
pytest -v
```

### Pruebas específicas
```bash
# Unitarias
pytest tests/test_servicios.py -v

# Seguridad (OWASP Top 10 2025)
pytest specs/test_seguridad.py -v

# E2E GUI
pytest test_gui_e2e.py -v
```

### Cobertura
```bash
pytest --cov=services --cov=models --cov=gui tests/
```

## 8. Estándares de Código

### naming
- `snake_case` para funciones y variables
- `PascalCase` para clases
- `UPPER_SNAKE` para constantes

### Docstrings
```python
def funcion(param: tipo) -> tipo_retorno:
    """
    Descripción breve.
    
    Args:
        param: Descripción del parámetro
    
    Returns:
        tipo_retorno: Descripción del retorno
    """
```

## 9. Seguridad Implementada

| OWASP Top 10 2021 | Implementación |
|-------------------|----------------|
| A01 - Broken Access Control | Verificación de roles en UI y servicios |
| A02 - Cryptographic Failures | bcrypt (12 rounds), no passwords en texto |
| A03 - Injection | SQLite parametrizado, validación de entrada |
| A04 - Insecure Design | Arquitectura limpia, separación de responsabilidades |
| A05 - Security Misconfiguration | Rate limiting, audit logging |
| A07 - Authentication Failures | Rate limiting (5 intentos, 5 min), bcrypt |
| A09 - Security Logging | Auditoria completa en logs/auditoria.log |

## 10. Contribución

1. Fork del repositorio
2. Crear branch: `git checkout -b feature/nueva-funcionalidad`
3. Implementar con tests
4. Commit con mensaje convencional
5. Push y Pull Request

---

**Desarrollador**: Diego Medardo Saavedra García  
**Institución**: ABACOM - Instituto de Capacitación Técnica  
**Licencia**: MIT