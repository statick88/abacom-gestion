"""
================================================================================
ESQUEMA DE BASE DE DATOS - SISTEMA DE GESTIÓN EDUCATIVA ABACOM
================================================================================
Base de datos: SQLite3
Instituto: ABACOM

Autor: Diego Medardo Saavedra García
Fecha: Abril 2026
================================================================================
"""

-- ============================================================================
-- TABLA: docentes
-- ============================================================================
-- Almacena información de los docentes/facilitadores del instituto

CREATE TABLE IF NOT EXISTS docentes (
    id_docente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres_completos TEXT NOT NULL,
    telefono TEXT,
    celular TEXT NOT NULL,
    correo_electronico TEXT NOT NULL UNIQUE,
    especializacion TEXT,
    estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'inactivo')),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(correo_electronico)
);

-- ============================================================================
-- TABLA: estudiantes
-- ============================================================================
-- Almacena información de los estudiantes registrados

CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
    identificacion TEXT NOT NULL UNIQUE,  -- Cédula de identidad Ecuador (10 dígitos)
    nombres_completos TEXT NOT NULL,
    telefono_fijo TEXT,
    celular TEXT NOT NULL,
    correo_electronico TEXT NOT NULL UNIQUE,
    direccion TEXT,
    fecha_nacimiento DATE,
    estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'inactivo', 'egresado')),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(identificacion),
    UNIQUE(correo_electronico)
);

-- ============================================================================
-- TABLA: cursos
-- ============================================================================
-- Almacena información de los cursos del instituto

CREATE TABLE IF NOT EXISTS cursos (
    id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,  -- ej: 01, 02, etc.
    nombre TEXT NOT NULL,
    descripcion TEXT,
    modalidad TEXT NOT NULL CHECK(modalidad IN ('Online', 'Virtual', 'Presencial')),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    horario_inicio TEXT NOT NULL,  -- ej: 19:00
    horario_fin TEXT NOT NULL,     -- eg: 22:00
    dias_semana TEXT NOT NULL,    -- eg: "Lunes,Martes,Miércoles,Jueves,Viernes"
    inversion DECIMAL(10, 2) NOT NULL,
    id_docente INTEGER,
    capacidad INTEGER DEFAULT 30,
    estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'cancelado', 'finalizado', 'en_curso')),
    periodo_academico INTEGER DEFAULT 2026,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_docente) REFERENCES docentes(id_docente),
    UNIQUE(codigo)
);

-- ============================================================================
-- TABLA: inscripciones
-- ============================================================================
-- Relaciona estudiantes con cursos y controla requisitos

CREATE TABLE IF NOT EXISTS inscripciones (
    id_inscripcion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_estudiante INTEGER NOT NULL,
    id_curso INTEGER NOT NULL,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tiene_pdf_cedula BOOLEAN DEFAULT 0,
    ruta_pdf_cedula TEXT,
    tiene_pago BOOLEAN DEFAULT 0,
    comprobante_pago TEXT,
    estado_certificacion TEXT DEFAULT 'pendiente' CHECK(
        estado_certificacion IN ('pendiente', 'en_proceso', 'aprobado', 'reprobado')
    ),
    calificacion REAL,
    observaciones TEXT,
    estado TEXT DEFAULT 'inscrito' CHECK(
        estado IN ('inscrito', 'cancelado', 'finalizado', 'certificado')
    ),
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso),
    UNIQUE(id_estudiante, id_curso)  -- Un estudiante no puede inscribirse dos veces al mismo curso
);

-- ============================================================================
-- TABLA: certificaciones
-- ============================================================================
-- Almacena certificados generados con aval del Ministerio del Trabajo

CREATE TABLE IF NOT EXISTS certificaciones (
    id_certificacion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_inscripcion INTEGER NOT NULL,
    numero_certificado TEXT NOT NULL UNIQUE,
    fecha_emision DATE NOT NULL,
    estado TEXT DEFAULT 'emitido' CHECK(estado IN ('emitido', 'entregado', 'anulado')),
    aval_ministerio TEXT DEFAULT 'Ministerio del Trabajo - Ecuador',
    url_certificado TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_inscripcion) REFERENCES inscripciones(id_inscripcion),
    UNIQUE(numero_certificado)
);

-- ============================================================================
-- TABLA: notificaciones
-- ============================================================================
-- Registro de notificaciones enviadas (30 minutos antes de clase)

CREATE TABLE IF NOT EXISTS notificaciones (
    id_notificacion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_curso INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('recordatorio_clase', 'inicio_curso', 'certificacion', 'aviso')),
    mensaje TEXT NOT NULL,
    fecha_programada TIMESTAMP NOT NULL,
    fecha_envio TIMESTAMP,
    estado TEXT DEFAULT 'pendiente' CHECK(estado IN ('pendiente', 'enviado', 'fallido', 'cancelado')),
    canal TEXT DEFAULT 'whatsapp' CHECK(canal IN ('whatsapp', 'email', 'sms')),
    destinatarios TEXT,  -- JSON con lista de destinatarios
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);

-- ============================================================================
-- TABLA: aulas_virtuales
-- ============================================================================
-- Almacena información de aulas virtuales y grupos de WhatsApp

CREATE TABLE IF NOT EXISTS aulas_virtuales (
    id_aula INTEGER PRIMARY KEY AUTOINCREMENT,
    id_curso INTEGER NOT NULL,
    plataforma TEXT DEFAULT 'Google Meet',
    link_reunion TEXT,
    grupo_whatsapp TEXT,
    link_grupo_whatsapp TEXT,
    estado TEXT DEFAULT 'creada' CHECK(estado IN ('creada', 'activa', 'cerrada')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);

-- ============================================================================
-- TABLA: configuration
-- ============================================================================
-- Configuración general del sistema

CREATE TABLE IF NOT EXISTS configuracion (
    id_config INTEGER PRIMARY KEY AUTOINCREMENT,
    clave TEXT NOT NULL UNIQUE,
    valor TEXT NOT NULL,
    descripcion TEXT,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(clave)
);

-- ============================================================================
-- INSERCIONES INICIALES DE CONFIGURACIÓN
-- ============================================================================

INSERT INTO configuracion (clave, valor, descripcion) VALUES
    ('periodo_academico_default', '2026', 'Período académico por defecto'),
    ('notificacion_minutos_antes', '30', 'Minutos antes de clase para enviar notificación'),
    ('hora_notificacion_default', '18:30', 'Hora por defecto para notificaciones'),
    ('calificacion_minima_aprobacion', '70', 'Nota mínima para aprobar curso'),
    ('institucion_nombre', 'ABACOM', 'Nombre del instituto'),
    ('institucion_razon_social', 'Instituto de Tecnología y Ciencias'),
    ('aval_ministerio', 'Ministerio del Trabajo - Ecuador', 'Aval para certificaciones');

-- ============================================================================
-- ÍNDICES PARA OPTIMIZAR CONSULTAS
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_estudiantes_cedula ON estudiantes(identificacion);
CREATE INDEX IF NOT EXISTS idx_estudiantes_correo ON estudiantes(correo_electronico);
CREATE INDEX IF NOT EXISTS idx_cursos_periodo ON cursos(periodo_academico);
CREATE INDEX IF NOT EXISTS idx_cursos_estado ON cursos(estado);
CREATE INDEX IF NOT EXISTS idx_inscripciones_estudiante ON inscripciones(id_estudiante);
CREATE INDEX IF NOT EXISTS idx_inscripciones_curso ON inscripciones(id_curso);
CREATE INDEX IF NOT EXISTS idx_notificaciones_curso ON notificaciones(id_curso);
CREATE INDEX IF NOT EXISTS idx_notificaciones_fecha ON notificaciones(fecha_programada);

-- ============================================================================
-- VISTAS ÚTILES
-- ============================================================================

-- Vista: Lista de estudiantes por curso con requisitos completos
CREATE VIEW IF NOT EXISTS v_estudiantes_por_curso AS
SELECT
    c.nombre AS nombre_curso,
    c.codigo AS codigo_curso,
    c.modalidad,
    c.fecha_inicio,
    c.fecha_fin,
    e.nombres_completos,
    e.identificacion,
    e.celular,
    e.correo_electronico,
    i.fecha_inscripcion,
    CASE
        WHEN i.tiene_pdf_cedula AND i.tiene_pago THEN 'COMPLETO'
        WHEN i.tiene_pdf_cedula THEN 'PENDIENTE PAGO'
        WHEN i.tiene_pago THEN 'PENDIENTE CEDULA'
        ELSE 'INCOMPLETO'
    END AS estado_requisitos,
    i.estado_certificacion,
    i.calificacion
FROM estudiantes e
JOIN inscripciones i ON e.id_estudiante = i.id_estudiante
JOIN cursos c ON i.id_curso = c.id_curso
WHERE i.estado = 'inscrito';

-- Vista: Cursos con información de inscripción
CREATE VIEW IF NOT EXISTS v_cursos_inscripciones AS
SELECT
    c.id_curso,
    c.codigo,
    c.nombre,
    c.modalidad,
    c.fecha_inicio,
    c.fecha_fin,
    c.horario_inicio,
    c.horario_fin,
    d.nombres_completos AS nombre_docente,
    COUNT(i.id_inscripcion) AS total_inscritos,
    c.capacidad,
    CASE
        WHEN COUNT(i.id_inscripcion) >= c.capacidad THEN 'LLENO'
        WHEN COUNT(i.id_inscripcion) > 0 THEN 'CON INSCRIPCIONES'
        ELSE 'SIN INSCRIPCIONES'
    END AS estado_inscripcion
FROM cursos c
LEFT JOIN docentes d ON c.id_docente = d.id_docente
LEFT JOIN inscripciones i ON c.id_curso = i.id_curso AND i.estado = 'inscrito'
GROUP BY c.id_curso;

-- ============================================================================
-- VERIFICACIÓN DEL ESQUEMA
-- ============================================================================

-- Verificar que las tablas fueron creadas
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;

-- Mostrar estructura de tablas
-- .schema estudiantes
-- .schema cursos
-- .schema inscripciones