# Seguridad - Sistema ABACOM

## Resumen de Seguridad

Este documento describe las medidas de seguridad implementadas en el sistema ABACOM, alineadas con el OWASP Top 10 2025.

---

## Medidas de Seguridad Implementadas

### A01 - Broken Access Control
- ✅ Roles definidos: admin, docente, estudiante
- ✅ Validación de estado de usuario en login
- ⚠️ RBAC implementado pero no enforced en GUI

### A02 - Security Misconfiguration
- ✅ SQLite con constraints CHECK
- ✅ Validación de entrada en todos los forms
- ✅ Prepared statements en queries

### A03 - Software Supply Chain
- ⚠️ Sin verificación de dependencias automática
- 📋 Pendiente: implementar audit de dependencias

### A04 - Cryptographic Failures ✅
- ✅ **bcrypt** con rounds=12 para hashing de contraseñas
- ✅ Salt automático por cada password
- ⚠️ Datos sensibles en BD no encriptados

### A05 - Injection
- ✅ Prepared statements en todas las queries
- ✅ Validación de entrada (cédula, email, teléfono)
- ⚠️ XSS no aplicable (desktop app)

### A06 - Insecure Design
- ✅ Spec-Driven Development (SDD) documentado
- ✅ 20 spec tests validando reglas de negocio

### A07 - Authentication Failures ✅
- ✅ **Rate limiting**: 5 intentos máximo, 5 minutos de lockout
- ✅ logging de intentos fallidos
- ✅ Sesión con timeout implícito

### A08 - Software or Data Integrity
- ⚠️ Sin verificación de integridad de datos
- 📋 Pendiente: implementar checksums

### A09 - Security Logging ✅
- ✅ Archivo `logs/auditoria.log` con eventos:
  - LOGIN_SUCCESS
  - LOGIN_FAIL
  - LOGIN_LOCKED
- ✅ Timestamp + IP + usuario + acción

### A10 - Mishandling of Exceptions
- ✅ Manejo de errores con try/except
- ⚠️ Mensajes de error genéricos

---

## Configuración de Seguridad

### Variables de Entorno

| Variable | Descripción | Requerido |
|----------|--------------|-----------|
| `ABACOM_ADMIN_PASSWORD` | Contraseña del admin | No (genera aleatoria) |
| `ABACOM_INITIALIZE_ADMIN` | Inicializar admin al iniciar | No |

### Uso en Producción

```bash
# Establecer contraseña segura del admin
export ABACOM_ADMIN_PASSWORD='MiContraseñaSegura123!'

# Para desarrollo - inicializar admin automáticamente
export ABACOM_INITIALIZE_ADMIN=true
python3 gui/app.py
```

---

## Pruebas de Seguridad

### Tests Disponibles

```bash
# Spec tests (reglas de negocio)
pytest specs/ -v

# Tests de seguridad
pytest specs/test_seguridad.py -v
```

### Cobertura de Seguridad

| Área | Tests |
|------|-------|
| Validación de password | ✅ |
| Hash bcrypt | ✅ |
| Rate limiting | ✅ |
| SQL Injection | ✅ (prepared statements) |
| XSS | N/A (desktop app) |

---

## Auditoría

### Log de Auditoría

Ubicación: `logs/auditoria.log`

Formato:
```
[YYYY-MM-DD HH:MM:SS] IP | USUARIO | ACCION | DETALLE
```

Ejemplos:
```
[2026-04-30 23:19:57] 127.0.0.1 | statick | LOGIN_SUCCESS | Inicio de sesión exitoso
[2026-04-30 23:20:05] 127.0.0.1 | statick | LOGIN_FAIL | Password incorrecta
```

---

## Vulnerabilidades Conocidas

| ID | Severidad | Descripción | Estado |
|----|-----------|-------------|--------|
| AUTH-001 | Alta | Sin 2FA/MFA | 📋 Pendiente |
| AUTH-002 | Media | Sesión sin timeout | 📋 Pendiente |
| DATA-001 | Media | Datos sensibles sin encriptar | 📋 Pendiente |
| RBAC-001 | Baja | Control de acceso no enforced | 📋 Pendiente |

---

## Contacto para Seguridad

Para reportar vulnerabilidades: dsaavedra88@gmail.com

---

*Documento actualizado: Abril 2026*
*Versión del sistema: 1.0.0*