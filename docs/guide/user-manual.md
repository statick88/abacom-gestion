# Manual de Usuario - ABACOM Gestión

## 1. Introducción

ABACOM Gestión es una aplicación de escritorio para la administración educativa del Instituto ABACOM.

## 2. Requisitos del Sistema

| Requisito | Mínimo | Recomendado |
|-----------|--------|-------------|
| Sistema Operativo | Windows 10 / macOS 11 / Ubuntu 20.04 | - |
| RAM | 4 GB | 8 GB |
| Espacio en disco | 500 MB | 1 GB |
| Resolución | 1280x720 | 1920x1080 |

## 3. Instalación

### Windows
1. Descargar `ABACOM_Gestion_Setup.exe` de Releases
2. Ejecutar el instalador
3. Seguir las instrucciones del asistente

### macOS
1. Descargar `ABACOM_Gestion_1.0.0.dmg`
2. Abrir el archivo y arrastrar la app a Aplicaciones

### Linux
1. Descargar `ABACOM_Gestion_1.0.0_amd64.deb`
2. Instalar con: `sudo dpkg -i ABACOM_Gestion_1.0.0_amd64.deb`

## 4. Primeros Pasos

### Iniciar Sesión
1. Ejecutar la aplicación
2. Ingresar credenciales proporcionadas por el administrador
3. El sistema limita a 5 intentos fallidos (5 minutos de bloqueo)

### Navegación
La interfaz cuenta con 6 módulos principales:
- **Estudiantes**: Gestión de registro de estudiantes
- **Docentes**: Administración de personal docente
- **Cursos**: Creación y gestión de cursos
- **Inscripciones**: Matriculación de estudiantes
- **Certificados**: Generación de certificados
- **Reportes**: Estadísticas del sistema

## 5. Módulos

### 5.1 Estudiantes
- **Registrar**: Agregar nuevos estudiantes (cédula válida Ecuador)
- **Buscar**: Filtrar por nombre o identificación
- **Editar**: Modificar datos del estudiante
- **Eliminar**: Desactivar registro

### 5.2 Docentes
- **Registrar**: Agregar nuevo personal docente
- **Asignar**: Asignar docentes a cursos
- **Gestionar**: Editar información de contacto

### 5.3 Cursos
- **Crear**: Nuevo curso con horarios, costos, modalidad
- **Editar**: Modificar parámetros del curso
- **Estado**: Activar/Desactivar curso

### 5.4 Inscripciones
- **Matricular**: Inscribir estudiante en curso
- **Pagos**: Registrar pagos de inscripción
- **Certificados**: Generar certificado al aprobar

### 5.5 Certificados
- **Generar**: Crear certificado con datos del estudiante
- **Validar**: Verificar autenticidad del certificado

### 5.6 Reportes
- Estadísticas de estudiantes, cursos, inscripciones
- Reportes de ingresos y certificaciones

## 6. Validaciones

### Cédula Ecuador
- 10 dígitos exactamente
- Provincia válida (01-24)
- Dígito verificador válido

### Teléfonos
- Celular: 10 dígitos, inicia con 09
- Fijo: 9 dígitos, inicia con 0

### Correo
- Formato estándar: usuario@dominio.com

## 7. Solución de Problemas

| Problema | Solución |
|----------|----------|
| No puedo iniciar sesión | Verificar credenciales o esperar 5 min si hay bloqueo |
| Error al registrar estudiante | Verificar que la cédula sea válida |
| La aplicación no responde | Cerrar y reopen la aplicación |
| Error de base de datos | Contactar al administrador |

## 8. Seguridad

- Contraseñas encriptadas con bcrypt
- Rate limiting: 5 intentos máximos
- Registro de auditoría de acciones

---

**Soporte**: soporte@abacom.edu.ec
**Versión**: 1.0.0