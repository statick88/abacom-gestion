"""
================================================================================
GENERACIÓN DE PDF - SISTEMA DE GESTIÓN ABACOM
================================================================================
Generación de formularios de inscripción y certificados en PDF.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.platypus import HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

# Configuración
OUTPUT_DIR = Path("pdfs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Estilos
styles = getSampleStyleSheet()

# Crear estilos personalizados
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=HexColor('#1a237e'),
    spaceAfter=30,
    alignment=TA_CENTER
)

subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=HexColor('#283593'),
    spaceAfter=20,
    alignment=TA_CENTER
)

# =============================================================================
# FUNCIÓN: GENERAR FORMULARIO DE INSCRIPCIÓN
# =============================================================================

def generar_formulario_inscripcion(
    id_inscripcion: int,
    datos_estudiante: Dict,
    datos_curso: Dict,
    output_path: Optional[str] = None
) -> str:
    """
    Genera un formulario de inscripción en PDF.
    
    Args:
        id_inscripcion: ID de la inscripción
        datos_estudiante: Diccionario con datos del estudiante
        datos_curso: Diccionario con datos del curso
        output_path: Ruta de salida (opcional)
    
    Returns:
        str: Ruta al archivo PDF generado
    """
    if output_path is None:
        output_path = str(OUTPUT_DIR / f"inscripcion_{id_inscripcion}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Contenido del documento
    story = []
    
    # Título
    story.append(Paragraph("FORMULARIO DE INSCRIPCIÓN", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Información del Instituto
    story.append(Paragraph("ABACOM - Instituto de Tecnología y Ciencias", subtitle_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Datos de la inscripción
    story.append(Paragraph(f"<b>Número de Inscripción:</b> {id_inscripcion}", styles['Normal']))
    story.append(Paragraph(f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Tabla de datos del estudiante
    story.append(Paragraph("<b>DATOS DEL ESTUDIANTE</b>", styles['Heading3']))
    
    data_est = [
        ["Cédula:", datos_estudiante.get('identificacion', '')],
        ["Nombres Completos:", datos_estudiante.get('nombres_completos', '')],
        ["Teléfono Fijo:", datos_estudiante.get('telefono_fijo', 'N/A')],
        ["Celular:", datos_estudiante.get('celular', '')],
        ["Correo Electrónico:", datos_estudiante.get('correo_electronico', '')],
    ]
    
    t_est = Table(data_est, colWidths=[3*cm, 12*cm])
    t_est.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_est)
    story.append(Spacer(1, 0.3*inch))
    
    # Tabla de datos del curso
    story.append(Paragraph("<b>DATOS DEL CURSO</b>", styles['Heading3']))
    
    data_cur = [
        ["Código:", datos_curso.get('codigo', '')],
        ["Nombre:", datos_curso.get('nombre', '')],
        ["Modalidad:", datos_curso.get('modalidad', '')],
        ["Fechas:", f"{datos_curso.get('fecha_inicio', '')} al {datos_curso.get('fecha_fin', '')}"],
        ["Horario:", f"{datos_curso.get('horario_inicio', '')} - {datos_curso.get('horario_fin', '')}"],
        ["Días:", datos_curso.get('dias_semana', '')],
        ["Inversión:", f"${datos_curso.get('inversion', 0):.2f}"],
    ]
    
    t_cur = Table(data_cur, colWidths=[3*cm, 12*cm])
    t_cur.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_cur)
    story.append(Spacer(1, 0.5*inch))
    
    # Requisitos
    story.append(Paragraph("<b>REQUISITOS</b>", styles['Heading3']))
    story.append(Paragraph("☑ Copia de cédula en PDF", styles['Normal']))
    story.append(Paragraph("☑ Comprobante de pago", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Firma
    story.append(Paragraph("<b>Firma del Estudiante:</b>", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    story.append(HRFlowable(width="100%"))
    story.append(Paragraph("Firma y cédula", styles['Normal']))
    
    # Construir PDF
    doc.build(story)
    
    return output_path

# =============================================================================
# FUNCIÓN: GENERAR CERTIFICADO
# =============================================================================

def generar_certificado_pdf(
    numero_certificado: str,
    nombre_estudiante: str,
    nombre_curso: str,
    calificacion: float,
    fecha_emision: str,
    output_path: Optional[str] = None
) -> str:
    """
    Genera un certificado en PDF con aval del Ministerio del Trabajo.
    
    Args:
        numero_certificado: Número único del certificado
        nombre_estudiante: Nombre del estudiante
        nombre_curso: Nombre del curso
        calificacion: Calificación obtenida
        fecha_emision: Fecha de emisión
        output_path: Ruta de salida (opcional)
    
    Returns:
        str: Ruta al archivo PDF generado
    """
    if output_path is None:
        output_path = str(OUTPUT_DIR / f"certificado_{numero_certificado}_{datetime.now().strftime('%Y%m%d')}.pdf")
    
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Fondo
    c.setFillColor(HexColor('#f5f5f5'))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Borde decorativo
    c.setStrokeColor(HexColor('#1a237e'))
    c.setLineWidth(3)
    c.rect(2*cm, 2*cm, width-4*cm, height-4*cm, fill=0, stroke=1)
    
    c.setLineWidth(1)
    c.rect(2.5*cm, 2.5*cm, width-5*cm, height-5*cm, fill=0, stroke=1)
    
    # Título
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(HexColor('#1a237e'))
    c.drawCentredString(width/2, height-4*cm, "CERTIFICADO")
    
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height-5*cm, "DE APROBACIÓN")
    
    # Cuerpo
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height-7*cm, "Se certifica que:")
    
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(HexColor('#283593'))
    c.drawCentredString(width/2, height-8*cm, nombre_estudiante)
    
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height-9.5*cm, f"Ha aprobado el curso:")
    
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height-10.5*cm, nombre_curso)
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height-11.5*cm, f"Con calificación: {calificacion:.1f}/100")
    
    # Aval
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(HexColor('#d32f2f'))
    c.drawCentredString(width/2, height-13*cm, "AVAL: MINISTERIO DEL TRABAJO - ECUADOR")
    
    # Número y fecha
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(3*cm, 3*cm, f"Certificado N°: {numero_certificado}")
    c.drawString(width-8*cm, 3*cm, f"Fecha: {fecha_emision}")
    
    # Guardar
    c.save()
    
    return output_path

# =============================================================================
# PRUEBA DE GENERACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=== Generador de PDF - ABACOM ===\n")
    
    # 1. Probar formulario de inscripción
    print("1. Generando formulario de inscripción...")
    datos_est = {
        'identificacion': '1712345678',
        'nombres_completos': 'Juan Pérez Test',
        'telefono_fijo': '02-1234567',
        'celular': '0991234567',
        'correo_electronico': 'juan@test.com'
    }
    datos_cur = {
        'codigo': 'PY101',
        'nombre': 'Python Fundamentos',
        'modalidad': 'Online',
        'fecha_inicio': '2026-05-01',
        'fecha_fin': '2026-06-15',
        'horario_inicio': '19:00',
        'horario_fin': '21:00',
        'dias_semana': 'Lunes,Miércoles,Viernes',
        'inversion': 150.0
    }
    
    pdf1 = generar_formulario_inscripcion(1, datos_est, datos_cur)
    print(f"   ✅ Formulario generado: {pdf1}")
    
    # 2. Probar certificado
    print("\n2. Generando certificado...")
    pdf2 = generar_certificado_pdf(
        numero_certificado="ABACOM-2026-A1B2C3D4",
        nombre_estudiante="Juan Pérez Test",
        nombre_curso="Python Fundamentos",
        calificacion=85.0,
        fecha_emision=datetime.now().strftime('%Y-%m-%d')
    )
    print(f"   ✅ Certificado generado: {pdf2}")
    
    print("\n✅ PDFs generados exitosamente")
