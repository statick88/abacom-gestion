"""
================================================================================
INTERFAZ GRAFICA REAL (PyQt5) - SISTEMA DE GESTION EDUCATIVA ABACOM
================================================================================
Migración de consola a PyQt5 (versión 5.15 instalada).

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QFormLayout,
    QDialog, QMessageBox, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from models.database import ejecutar_consulta, ejecutar_modificacion
from models.entities import Estudiante, Curso, Inscripcion, Certificado
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
# VENTANA PRINCIPAL
# =============================================================================

class ABACOMGUI(QMainWindow):
    """Aplicación principal GUI para ABACOM."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ABACOM - Sistema de Gestión Educativa")
        self.setGeometry(100, 100, 900, 600)
        
        self.setup_ui()
        self.load_stats()
        
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Título
        title_label = QLabel("🎓 SISTEMA DE GESTION ABACOM")
        title_font = QFont("Helvetica", 20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Instituto de Tecnología y Ciencias")
        subtitle_font = QFont("Helvetica", 12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        # Botones principales
        btn_layout = QHBoxLayout()
        
        # Estudiantes
        btn_est = QPushButton("👨 Estudiantes")
        btn_est.clicked.connect(self.open_estudiantes)
        btn_layout.addWidget(btn_est)
        
        # Cursos
        btn_cur = QPushButton("📚 Cursos")
        btn_cur.clicked.connect(self.open_cursos)
        btn_layout.addWidget(btn_cur)
        
        # Inscripciones
        btn_ins = QPushButton("📝 Inscripciones")
        btn_ins.clicked.connect(self.open_inscripciones)
        btn_layout.addWidget(btn_ins)
        
        # Certificados
        btn_cert = QPushButton("🏆 Certificados")
        btn_cert.clicked.connect(self.open_certificados)
        btn_layout.addWidget(btn_cert)
        
        # Reportes
        btn_rep = QPushButton("📊 Reportes")
        btn_rep.clicked.connect(self.open_reportes)
        btn_layout.addWidget(btn_rep)
        
        main_layout.addLayout(btn_layout)
        
        # Área de información
        self.stats_label = QLabel()
        self.stats_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.stats_label)
        
        # Barra de estado
        self.statusBar().showMessage("✅ Sistema listo")
        
    def load_stats(self):
        """Carga estadísticas rápidas."""
        estudiantes = listar_estudiantes()
        cursos = listar_cursos()
        
        stats_text = f"""
        📊 Estadísticas Rápidas:
        
        • Total Estudiantes: {len(estudiantes)}
        • Total Cursos: {len(cursos)}
        • Base de Datos: Conectada ✅
        • Versión: 1.0.0
        • Autor: Diego Medardo Saavedra García
        """
        self.stats_label.setText(stats_text)
        
    def open_estudiantes(self):
        """Abre la ventana de gestión de estudiantes."""
        self.estudiantes_window = EstudiantesWindow(self)
        self.estudiantes_window.show()
        
    def open_cursos(self):
        """Abre la ventana de gestión de cursos."""
        self.cursos_window = CursosWindow(self)
        self.cursos_window.show()
        
    def open_inscripciones(self):
        """Abre la ventana de inscripciones."""
        QMessageBox.information(self, "Inscripciones", 
            "Función en desarrollo...\n\nPróximamente disponible.")
        
    def open_certificados(self):
        """Abre la ventana de certificados."""
        QMessageBox.information(self, "Certificados", 
            "Función en desarrollo...\n\nPróximamente disponible.")
        
    def open_reportes(self):
        """Abre la ventana de reportes."""
        QMessageBox.information(self, "Reportes", 
            "Función en desarrollo...\n\nPróximamente disponible.")

# =============================================================================
# VENTANA: ESTUDIANTES
# =============================================================================

class EstudiantesWindow(QWidget):
    """Ventana de gestión de estudiantes."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("👨 Gestión de Estudiantes")
        self.setGeometry(100, 100, 800, 500)
        
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Configura la interfaz."""
        layout = QVBoxLayout(self)
        
        # Botones superiores
        top_layout = QHBoxLayout()
        
        btn_new = QPushButton("➕ Nuevo Estudiante")
        btn_new.clicked.connect(self.new_estudiante)
        top_layout.addWidget(btn_new)
        
        btn_refresh = QPushButton("🔄 Actualizar")
        btn_refresh.clicked.connect(self.load_data)
        top_layout.addWidget(btn_refresh)
        
        top_layout.addStretch()
        layout.addLayout(top_layout)
        
        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Cédula", "Nombres", "Celular", "Correo"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        
        # Doble clic para ver detalles
        self.table.cellDoubleClicked.connect(self.view_estudiante)
        
    def load_data(self):
        """Carga los datos en la tabla."""
        self.table.setRowCount(0)  # Limpiar tabla
        
        estudiantes = listar_estudiantes()
        
        for est in estudiantes:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(str(est['id_estudiante'])))
            self.table.setItem(row, 1, QTableWidgetItem(est['identificacion']))
            self.table.setItem(row, 2, QTableWidgetItem(est['nombres_completos']))
            self.table.setItem(row, 3, QTableWidgetItem(est['celular']))
            self.table.setItem(row, 4, QTableWidgetItem(est['correo_electronico']))
            
    def new_estudiante(self):
        """Abre formulario para nuevo estudiante."""
        self.form = EstudianteForm(self, callback=self.load_data)
        self.form.show()
        
    def view_estudiante(self):
        """Ver detalles del estudiante seleccionado."""
        current_row = self.table.currentRow()
        if current_row < 0:
            return
            
        id_est = int(self.table.item(current_row, 0).text())
        
        # Obtener datos completos
        query = "SELECT * FROM estudiantes WHERE id_estudiante = ?"
        result = ejecutar_consulta(query, (id_est,))
        
        if result:
            est = result[0]
            info = f"""
            ID: {est['id_estudiante']}
            Cédula: {est['identificacion']}
            Nombres: {est['nombres_completos']}
            Teléfono: {est['telefono_fijo'] or 'N/A'}
            Celular: {est['celular']}
            Correo: {est['correo_electronico']}
            Estado: {est['estado']}
            """
            QMessageBox.information(self, "Detalles del Estudiante", info)

# =============================================================================
# FORMULARIO: ESTUDIANTE
# =============================================================================

class EstudianteForm(QDialog):
    """Formulario para crear/editar estudiante."""
    
    def __init__(self, parent=None, id_estudiante=None, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.id_estudiante = id_estudiante
        
        self.setWindowTitle("➕ Nuevo Estudiante" if not id_estudiante else "✏ Editar Estudiante")
        self.setGeometry(100, 100, 500, 400)
        
        self.setup_ui()
        
        if id_estudiante:
            self.load_estudiante()
            
    def setup_ui(self):
        """Configura el formulario."""
        layout = QFormLayout(self)
        
        # Cédula
        self.cedula_edit = QLineEdit()
        layout.addRow("Cédula de Identidad:", self.cedula_edit)
        
        # Nombres
        self.nombres_edit = QLineEdit()
        layout.addRow("Nombres Completos:", self.nombres_edit)
        
        # Teléfono fijo
        self.telefono_edit = QLineEdit()
        layout.addRow("Teléfono Fijo:", self.telefono_edit)
        
        # Celular
        self.celular_edit = QLineEdit()
        layout.addRow("Celular:", self.celular_edit)
        
        # Correo
        self.correo_edit = QLineEdit()
        layout.addRow("Correo Electrónico:", self.correo_edit)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        btn_save = QPushButton("✅ Guardar")
        btn_save.clicked.connect(self.save_estudiante)
        btn_layout.addWidget(btn_save)
        
        btn_cancel = QPushButton("❌ Cancelar")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        
        layout.addRow(btn_layout)
        
        # Enfocar en cédula
        self.cedula_edit.setFocus()
        
    def load_estudiante(self):
        """Carga datos del estudiante para edición."""
        query = "SELECT * FROM estudiantes WHERE id_estudiante = ?"
        result = ejecutar_consulta(query, (self.id_estudiante,))
        
        if result:
            est = result[0]
            self.cedula_edit.setText(est['identificacion'])
            self.nombres_edit.setText(est['nombres_completos'])
            self.telefono_edit.setText(est['telefono_fijo'] or '')
            self.celular_edit.setText(est['celular'])
            self.correo_edit.setText(est['correo_electronico'])
            
    def save_estudiante(self):
        """Guarda el estudiante."""
        cedula = self.cedula_edit.text().strip()
        nombres = self.nombres_edit.text().strip()
        telefono = self.telefono_edit.text().strip() or None
        celular = self.celular_edit.text().strip()
        correo = self.correo_edit.text().strip()
        
        # Validaciones
        if not cedula or not validar_cedula_ecuador(cedula):
            QMessageBox.critical(self, "Error", "Cédula inválida. Debe tener 10 dígitos.")
            return
            
        if not nombres:
            QMessageBox.critical(self, "Error", "Nombres son requeridos.")
            return
            
        if not celular:
            QMessageBox.critical(self, "Error", "Celular es requerido.")
            return
            
        if not correo:
            QMessageBox.critical(self, "Error", "Correo es requerido.")
            return
            
        # Guardar
        result = registrar_estudiante(
            identificacion=cedula,
            nombres_completos=nombres,
            celular=celular,
            correo_electronico=correo,
            telefono_fijo=telefono
        )
        
        if result['exito']:
            QMessageBox.information(self, "Éxito", result['mensaje'])
            if self.callback:
                self.callback()
            self.accept()
        else:
            QMessageBox.critical(self, "Error", result['error'])

# =============================================================================
# VENTANA: CURSOS (Simplificada)
# =============================================================================

class CursosWindow(QWidget):
    """Ventana de gestión de cursos."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📚 Gestión de Cursos")
        self.setGeometry(100, 100, 800, 500)
        
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Configura la interfaz."""
        layout = QVBoxLayout(self)
        
        # Botones
        top_layout = QHBoxLayout()
        
        btn_new = QPushButton("➕ Nuevo Curso")
        btn_new.clicked.connect(self.new_curso)
        top_layout.addWidget(btn_new)
        
        btn_refresh = QPushButton("🔄 Actualizar")
        btn_refresh.clicked.connect(self.load_data)
        top_layout.addWidget(btn_refresh)
        
        top_layout.addStretch()
        layout.addLayout(top_layout)
        
        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Código", "Nombre", "Inicio", "Estado"])
        layout.addWidget(self.table)
        
    def load_data(self):
        """Carga los cursos."""
        self.table.setRowCount(0)
        
        cursos = listar_cursos()
        
        for cur in cursos:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(str(cur['id_curso'])))
            self.table.setItem(row, 1, QTableWidgetItem(cur['codigo']))
            self.table.setItem(row, 2, QTableWidgetItem(cur['nombre']))
            self.table.setItem(row, 3, QTableWidgetItem(str(cur['fecha_inicio'])))
            self.table.setItem(row, 4, QTableWidgetItem(cur['estado']))
            
    def new_curso(self):
        """Abre formulario de curso."""
        QMessageBox.information(self, "Nuevo Curso", 
            "Función en desarrollo...\n\nPróximamente disponible.")

# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ABACOMGUI()
    window.show()
    sys.exit(app.exec_())
