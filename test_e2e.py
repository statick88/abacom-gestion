"""
Test end-to-end del sistema ABACOM
"""
import sys
sys.path.insert(0, '/Users/statick/dev/apps/abacom/course_of_python/abacom-gestion')

from models.database import ejecutar_modificacion

# Cleanup before test
print("Limpiando datos de prueba...")
tables = ['certificaciones', 'inscripciones', 'estudiantes', 'cursos']
for table in tables:
    try:
        ejecutar_modificacion(f'DELETE FROM {table}')
    except:
        pass
print("✅ Datos limpios\n")

from services.servicios import (
    validar_cedula_ecuador,
    registrar_estudiante,
    listar_estudiantes,
    registrar_curso,
    listar_cursos,
    inscribir_estudiante,
    generar_certificado,
    calcular_hora_notificacion
)

print("="*60)
print("TEST END-TO-END - SISTEMA ABACOM")
print("="*60)

# 1. Validar cédula
print("\n1. Validación de cédula Ecuador...")
assert validar_cedula_ecuador("1712345678") == True
assert validar_cedula_ecuador("0012345678") == False
assert validar_cedula_ecuador("1712345") == False
print("   ✅ Validación OK")

# 2. Registrar estudiante
print("\n2. Registrando estudiante...")
result = registrar_estudiante(
    identificacion="1712345678",
    nombres_completos="Juan Pérez Test",
    celular="0991234567",
    correo_electronico="juan.test@email.com"
)
assert result["exito"] == True
id_estudiante = result["id_estudiante"]
print(f"   ✅ Estudiante registrado con ID: {id_estudiante}")

# 3. Listar estudiantes
print("\n3. Listando estudiantes...")
estudiantes = listar_estudiantes()
assert len(estudiantes) > 0
print(f"   ✅ Total estudiantes: {len(estudiantes)}")

# 4. Registrar curso
print("\n4. Registrando curso...")
result = registrar_curso(
    codigo="PY101",
    nombre="Python Fundamentos",
    modalidad="Online",
    fecha_inicio="2026-05-01",
    fecha_fin="2026-06-15",
    horario_inicio="19:00",
    horario_fin="21:00",
    dias_semana="Lunes,Miércoles,Viernes",
    inversion=150.0
)
assert result["exito"] == True
id_curso = result["id_curso"]
print(f"   ✅ Curso registrado con ID: {id_curso}")
print(f"   Duración: {result['duracion_semanas']} semanas")

# 5. Listar cursos
print("\n5. Listando cursos...")
cursos = listar_cursos()
assert len(cursos) > 0
print(f"   ✅ Total cursos: {len(cursos)}")

# 6. Inscribir estudiante en curso
print("\n6. Inscribiendo estudiante en curso...")
result = inscribir_estudiante(
    id_estudiante=id_estudiante,
    id_curso=id_curso,
    tiene_pdf_cedula=True,
    tiene_pago=True
)
assert result["exito"] == True
id_inscripcion = result["id_inscripcion"]
print(f"   ✅ Inscripción exitosa con ID: {id_inscripcion}")

# 7. Calcular notificación
print("\n7. Calculando hora de notificación...")
hora_notif = calcular_hora_notificacion("19:00")
assert hora_notif == "18:30"
print(f"   ✅ Notificación a las {hora_notif} (30 min antes)")

# 8. Generar certificado
print("\n8. Generando certificado...")
result = generar_certificado(
    id_inscripcion=id_inscripcion,
    calificacion=85.0
)
assert result["exito"] == True
print(f"   ✅ Certificado: {result['numero_certificado']}")
print(f"   Estado: {result['estado']}")
print(f"   Aval: {result['aval_ministerio']}")
print(f"   PDF: {result['pdf_path']}")

print("\n" + "="*60)
print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
print("="*60)
