"""
================================================================================
CONFIGURACIÓN DEL SISTEMA DE GESTIÓN ABACOM
================================================================================
"""

import os

# Obtener la ruta absoluta del directorio del proyecto (abacom-gestion)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, "database", "abacom.db")

# Configuración de la aplicación
APP_NAME = "Sistema de Gestión ABACOM"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Diego Medardo Saavedra García"
APP_INSTITUTO = "ABACOM - Instituto de Tecnología y Ciencias"

# Período académico por defecto
PERIODO_ACADEMICO_DEFAULT = 2026

# Configuración de notificaciones
NOTIFICACION_MINUTOS_ANTES = 30
HORA_NOTIFICACION_DEFAULT = "18:30"

# Configuración de certificaciones
CALIFICACION_MINIMA_APROBACION = 70
AVAL_MINISTERIO = "Ministerio del Trabajo - Ecuador"