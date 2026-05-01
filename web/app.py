"""
================================================================================
INTERFAZ WEB (FLASK) - SISTEMA DE GESTIÓN ABACOM
================================================================================
Interfaz web moderna usando Flask + HTML + CSS.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS

from models.database import ejecutar_consulta, ejecutar_modificacion
from services.servicios import (
    validar_cedula_ecuador,
    registrar_estudiante,
    listar_estudiantes,
    registrar_curso,
    listar_cursos,
    inscribir_estudiante,
    generar_certificado
)

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

app = Flask(__name__)
CORS(app)

# =============================================================================
# RUTAS PRINCIPALES
# =============================================================================

@app.route('/')
def index():
    """Página principal."""
    estudiantes = listar_estudiantes()
    cursos = listar_cursos()
    
    return render_template('index.html', 
        total_estudiantes=len(estudiantes),
        total_cursos=len(cursos)
    )

# =============================================================================
# API: ESTUDIANTES
# =============================================================================

@app.route('/api/estudiantes', methods=['GET'])
def get_estudiantes():
    """Obtiene todos los estudiantes."""
    estudiantes = listar_estudiantes()
    return jsonify(estudiantes)

@app.route('/api/estudiantes', methods=['POST'])
def create_estudiante():
    """Crea un nuevo estudiante."""
    data = request.json
    
    if not validar_cedula_ecuador(data.get('identificacion', '')):
        return jsonify({'exito': False, 'error': 'Cédula inválida'}), 400
    
    result = registrar_estudiante(
        identificacion=data['identificacion'],
        nombres_completos=data['nombres_completos'],
        celular=data['celular'],
        correo_electronico=data['correo_electronico'],
        telefono_fijo=data.get('telefono_fijo'),
        direccion=data.get('direccion')
    )
    
    return jsonify(result), 201 if result['exito'] else 400

# =============================================================================
# API: CURSOS
# =============================================================================

@app.route('/api/cursos', methods=['GET'])
def get_cursos():
    """Obtiene todos los cursos."""
    cursos = listar_cursos()
    return jsonify(cursos)

@app.route('/api/cursos', methods=['POST'])
def create_curso():
    """Crea un nuevo curso."""
    data = request.json
    
    result = registrar_curso(
        codigo=data['codigo'],
        nombre=data['nombre'],
        modalidad=data.get('modalidad', 'Online'),
        fecha_inicio=data['fecha_inicio'],
        fecha_fin=data['fecha_fin'],
        horario_inicio=data['horario_inicio'],
        horario_fin=data['horario_fin'],
        dias_semana=data['dias_semana'],
        inversion=float(data.get('inversion', 0))
    )
    
    return jsonify(result), 201 if result['exito'] else 400

# =============================================================================
# API: INSCRIPCIONES
# =============================================================================

@app.route('/api/inscripciones', methods=['POST'])
def create_inscripcion():
    """Inscribe un estudiante en un curso."""
    data = request.json
    
    result = inscribir_estudiante(
        id_estudiante=int(data['id_estudiante']),
        id_curso=int(data['id_curso']),
        tiene_pdf_cedula=data.get('tiene_pdf_cedula', False),
        tiene_pago=data.get('tiene_pago', False)
    )
    
    return jsonify(result), 200 if result['exito'] else 400

# =============================================================================
# API: CERTIFICADOS
# =============================================================================

@app.route('/api/certificados', methods=['POST'])
def create_certificado():
    """Genera un certificado."""
    data = request.json
    
    result = generar_certificado(
        id_inscripcion=int(data['id_inscripcion']),
        calificacion=float(data['calificacion'])
    )
    
    return jsonify(result), 200 if result['exito'] else 400

# =============================================================================
# INICIAR SERVIDOR
# =============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🎓 ABACOM - Sistema de Gestión Educativa")
    print("  Interfaz Web: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
