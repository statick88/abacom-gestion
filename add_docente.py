import sys
sys.path.insert(0, '.')

from models.database import ejecutar_modificacion, ejecutar_consulta

# Insert sample docente
try:
    id_doc = ejecutar_modificacion(
        """INSERT INTO docentes (nombres_completos, celular, correo_electronico, especializacion) 
           VALUES (?, ?, ?, ?)""",
        ('Diego Saavedra', '0991234567', 'diego@abacom.edu.ec', 'Python, Ciberseguridad')
    )
    print(f'✅ Docente created with ID: {id_doc}')
except Exception as e:
    print(f'Error inserting docente: {e}')

# Assign docente to first course
result = ejecutar_consulta('SELECT id_curso FROM cursos LIMIT 1')
if result:
    id_curso = result[0]['id_curso']
    ejecutar_modificacion(
        'UPDATE cursos SET id_docente = ? WHERE id_curso = ?',
        (1, id_curso)  # Use docente ID 1
    )
    print(f'✅ Docente assigned to course {id_curso}')
