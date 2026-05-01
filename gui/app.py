"""
================================================================================
INTERFAZ GRAFICA CON TKINTER - SISTEMA DE GESTIÓN EDUCATIVA ABACOM
================================================================================
Aplicación de escritorio usando tkinter (builtin de Python).

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional, List, Dict

from services.servicios import (
    validar_cedula_ecuador,
    registrar_estudiante,
    listar_estudiantes,
    registrar_curso,
    listar_cursos,
    inscribir_estudiante,
    generar_certificado,
    registrar_docente,
    listar_docentes,
    listar_inscripciones,
    listar_certificaciones,
    obtener_estadisticas,
    buscar_estudiantes,
    buscar_cursos
)


# =============================================================================
# CLASE PRINCIPAL - VENTANA DE LA APLICACIÓN
# =============================================================================

class ABACOMGUI:
    """Aplicación principal GUI para ABACOM usando tkinter."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ABACOM - Sistema de Gestión Educativa")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Estilos
        self.setup_styles()
        
        # UI principal
        self.create_header()
        self.create_main_menu()
        self.create_status_bar()
        
        # Cargar estadísticas iniciales
        self.actualizar_estadisticas()
        
    def setup_styles(self):
        """Configura estilos de la aplicación."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        self.colors = {
            'primary': '#1a237e',
            'secondary': '#283593',
            'accent': '#3949ab',
            'bg': '#f5f5f5',
            'success': '#4caf50',
            'warning': '#ff9800',
            'danger': '#f44336'
        }
        
        # Estilo para botones
        style.configure('Primary.TButton', font=('Helvetica', 10, 'bold'), padding=10)
        style.configure('Success.TButton', background=self.colors['success'], foreground='white')
        
    def create_header(self):
        """Crea el encabezado de la aplicación."""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Título
        title_label = tk.Label(
            header_frame,
            text="🎓 SISTEMA DE GESTIÓN ABACOM",
            font=('Helvetica', 22, 'bold'),
            fg='white',
            bg=self.colors['primary']
        )
        title_label.pack(pady=15)
        
        # Subtítulo
        subtitle_label = tk.Label(
            header_frame,
            text="Instituto de Tecnología y Ciencias",
            font=('Helvetica', 10),
            fg='#b3e5fc',
            bg=self.colors['primary']
        )
        subtitle_label.pack()
        
    def create_main_menu(self):
        """Crea el menú principal con botones."""
        menu_frame = tk.Frame(self.root, bg=self.colors['bg'])
        menu_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título del menú
        tk.Label(
            menu_frame,
            text="📋 MENÚ PRINCIPAL",
            font=('Helvetica', 16, 'bold'),
            bg=self.colors['bg']
        ).pack(pady=(0, 20))
        
        # Grid de botones
        buttons = [
            ("👨‍🎓 Estudiantes", self.open_estudiantes),
            ("👨‍🏫 Docentes", self.open_docentes),
            ("📚 Cursos", self.open_cursos),
            ("📝 Inscripciones", self.open_inscripciones),
            ("🏆 Certificados", self.open_certificados),
            ("📊 Reportes", self.open_reportes),
        ]
        
        # Crear grid 2x3
        for i, (text, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                menu_frame,
                text=text,
                font=('Helvetica', 14),
                width=20,
                height=2,
                bg=self.colors['secondary'],
                fg='white',
                cursor='hand2',
                command=command,
                relief='flat'
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
        # Panel de estadísticas
        stats_frame = tk.LabelFrame(
            menu_frame,
            text="📊 ESTADÍSTICAS",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['bg'],
            padx=10,
            pady=10
        )
        stats_frame.pack(fill='x', pady=20)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Cargando...",
            font=('Courier', 10),
            bg=self.colors['bg'],
            justify='left'
        )
        self.stats_label.pack(fill='x')
        
    def create_status_bar(self):
        """Crea la barra de estado."""
        status_frame = tk.Frame(self.root, bg='#333', height=30)
        status_frame.pack(fill='x')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="✅ Sistema listo",
            font=('Helvetica', 9),
            fg='white',
            bg='#333',
            anchor='w'
        )
        self.status_label.pack(side='left', padx=10)
        
        version_label = tk.Label(
            status_frame,
            text="v1.0.0 | Diego Medardo Saavedra García",
            font=('Helvetica', 8),
            fg='#aaa',
            bg='#333'
        )
        version_label.pack(side='right', padx=10)
        
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas en el panel."""
        stats = obtener_estadisticas()
        
        texto = f"""
   Estudiantes: {stats['total_estudiantes']}  |  Docentes: {stats['total_docentes']}
   Cursos: {stats['total_cursos']}  |  Inscripciones: {stats['total_inscripciones']}
   Certificados Emitidos: {stats['total_certificados']}
        """
        self.stats_label.config(text=texto)
        
    def open_estudiantes(self):
        """Abre ventana de gestión de estudiantes."""
        self.ventana_activa = VentanaEstudiantes(self.root)
        
    def open_docentes(self):
        """Abre ventana de gestión de docentes."""
        self.ventana_activa = VentanaDocentes(self.root)
        
    def open_cursos(self):
        """Abre ventana de gestión de cursos."""
        self.ventana_activa = VentanaCursos(self.root)
        
    def open_inscripciones(self):
        """Abre ventana de inscripciones."""
        self.ventana_activa = VentanaInscripciones(self.root)
        
    def open_certificados(self):
        """Abre ventana de certificados."""
        self.ventana_activa = VentanaCertificados(self.root)
        
    def open_reportes(self):
        """Abre ventana de reportes."""
        self.ventana_activa = VentanaReportes(self.root)


# =============================================================================
# VENTANA: ESTUDIANTES
# =============================================================================

class VentanaEstudiantes:
    """Ventana de gestión de estudiantes."""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("👨‍🎓 Gestión de Estudiantes")
        self.window.geometry("900x550")
        
        # Frame principal
        main_frame = tk.Frame(self.window, bg='#f5f5f5')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        tk.Label(
            main_frame,
            text="👨‍🎓 GESTIÓN DE ESTUDIANTES",
            font=('Helvetica', 14, 'bold'),
            bg='#f5f5f5'
        ).pack(pady=10)
        
        # Botones superiores
        btn_frame = tk.Frame(main_frame, bg='#f5f5f5')
        btn_frame.pack(fill='x', pady=5)
        
        tk.Button(btn_frame, text="➕ Nuevo Estudiante", command=self.nuevo_estudiante,
                  bg='#4caf50', fg='white', font=('Helvetica', 10)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_datos,
                  bg='#2196f3', fg='white', font=('Helvetica', 10)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🔍 Buscar", command=self.buscar_estudiante,
                  bg='#ff9800', fg='white', font=('Helvetica', 10)).pack(side='left', padx=5)
        
        # Tabla
        columns = ('ID', 'Cédula', 'Nombres', 'Teléfono', 'Celular', 'Correo', 'Estado')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=18)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != 'Nombres' else 180)
        
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Cargar datos
        self.cargar_datos()
        
    def cargar_datos(self):
        """Carga los datos en la tabla."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        estudiantes = listar_estudiantes()
        for est in estudiantes:
            self.tree.insert('', 'end', values=(
                est['id_estudiante'],
                est['identificacion'],
                est['nombres_completos'],
                est['telefono_fijo'] or 'N/A',
                est['celular'],
                est['correo_electronico'],
                est['estado']
            ))
    
    def nuevo_estudiante(self):
        """Abre formulario para nuevo estudiante."""
        form = FormularioEstudiante(self.window)
        if form.result:
            self.cargar_datos()
    
    def buscar_estudiante(self):
        """Busca estudiante por texto."""
        texto = simpledialog.askstring("Buscar", "Ingrese nombre, cédula o correo:")
        if texto:
            resultados = buscar_estudiantes(texto)
            if resultados:
                for item in self.tree.get_children():
                    self.tree.delete(item)
                for est in resultados:
                    self.tree.insert('', 'end', values=(
                        est['id_estudiante'],
                        est['identificacion'],
                        est['nombres_completos'],
                        est['telefono_fijo'] or 'N/A',
                        est['celular'],
                        est['correo_electronico'],
                        est['estado']
                    ))
            else:
                messagebox.showinfo("Buscar", "No se encontraron resultados")


class FormularioEstudiante:
    """Formulario para registrar estudiante."""
    
    def __init__(self, parent):
        self.result = None
        
        self.window = tk.Toplevel(parent)
        self.window.title("➕ Nuevo Estudiante")
        self.window.geometry("450x400")
        self.window.transient(parent)
        self.window.grab_set()
        
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Campos
        labels = ['Cédula:', 'Nombres Completos:', 'Teléfono Fijo:', 'Celular:', 'Correo:']
        self.entries = {}
        
        for i, label in enumerate(labels):
            tk.Label(main_frame, text=label, font=('Helvetica', 10)).grid(
                row=i, column=0, sticky='w', pady=5)
            
            entry = tk.Entry(main_frame, width=35, font=('Helvetica', 10))
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[label.replace(':', '').lower().replace(' ', '_')] = entry
        
        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="✅ Guardar", command=self.guardar,
                  bg='#4caf50', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=self.window.destroy,
                  bg='#f44336', fg='white', width=12).pack(side='left', padx=5)
        
        self.entries['nombres_completos'].focus()
    
    def guardar(self):
        """Guarda el estudiante."""
        datos = {}
        for key, entry in self.entries.items():
            datos[key] = entry.get().strip()
        
        if not datos['nombres_completos'] or not datos['celular'] or not datos['correo_electronico']:
            messagebox.showerror("Error", "Los campos nombres, celular y correo son requeridos")
            return
        
        if not validar_cedula_ecuador(datos['cedula']):
            messagebox.showerror("Error", "Cédula inválida. Debe tener 10 dígitos")
            return
        
        result = registrar_estudiante(
            identificacion=datos['cedula'],
            nombres_completos=datos['nombres_completos'],
            telefono_fijo=datos['telefono_fijo'] or None,
            celular=datos['celular'],
            correo_electronico=datos['correo_electronico']
        )
        
        if result['exito']:
            messagebox.showinfo("Éxito", result['mensaje'])
            self.result = True
            self.window.destroy()
        else:
            messagebox.showerror("Error", result['error'])


# =============================================================================
# VENTANA: DOCENTES
# =============================================================================

class VentanaDocentes:
    """Ventana de gestión de docentes."""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("👨‍🏫 Gestión de Docentes")
        self.window.geometry("900x550")
        
        main_frame = tk.Frame(self.window, bg='#f5f5f5')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="👨‍🏫 GESTIÓN DE DOCENTES",
                font=('Helvetica', 14, 'bold'), bg='#f5f5f5').pack(pady=10)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg='#f5f5f5')
        btn_frame.pack(fill='x', pady=5)
        
        tk.Button(btn_frame, text="➕ Nuevo Docente", command=self.nuevo_docente,
                  bg='#4caf50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_datos,
                  bg='#2196f3', fg='white').pack(side='left', padx=5)
        
        # Tabla
        columns = ('ID', 'Nombres', 'Teléfono', 'Celular', 'Correo', 'Especialización', 'Estado')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=18)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if 'Nombres' not in col else 150)
        
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.cargar_datos()
    
    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for doc in listar_docentes():
            self.tree.insert('', 'end', values=(
                doc['id_docente'], doc['nombres_completos'],
                doc['telefono'] or 'N/A', doc['celular'],
                doc['correo_electronico'], doc['especializacion'] or 'N/A',
                doc['estado']
            ))
    
    def nuevo_docente(self):
        form = FormularioDocente(self.window)
        if form.result:
            self.cargar_datos()


class FormularioDocente:
    def __init__(self, parent):
        self.result = None
        self.window = tk.Toplevel(parent)
        self.window.title("➕ Nuevo Docente")
        self.window.geometry("400x350")
        self.window.transient(parent)
        self.window.grab_set()
        
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        labels = ['Nombres:', 'Teléfono:', 'Celular:', 'Correo:', 'Especialización:']
        self.entries = {}
        
        for i, label in enumerate(labels):
            tk.Label(main_frame, text=label).grid(row=i, column=0, sticky='w', pady=5)
            entry = tk.Entry(main_frame, width=30)
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[label.replace(':', '').lower()] = entry
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=len(labels), columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="✅ Guardar", command=self.guardar,
                  bg='#4caf50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=self.window.destroy,
                  bg='#f44336', fg='white').pack(side='left', padx=5)
    
    def guardar(self):
        datos = {k: v.get().strip() for k, v in self.entries.items()}
        
        if not datos['nombres'] or not datos['celular'] or not datos['correo']:
            messagebox.showerror("Error", "Nombres, celular y correo son requeridos")
            return
        
        result = registrar_docente(
            nombres_completos=datos['nombres'],
            telefono=datos['teléfono'] or None,
            celular=datos['celular'],
            correo_electronico=datos['correo'],
            especializacion=datos['especialización'] or None
        )
        
        if result['exito']:
            messagebox.showinfo("Éxito", result['mensaje'])
            self.result = True
            self.window.destroy()
        else:
            messagebox.showerror("Error", result['error'])


# =============================================================================
# VENTANA: CURSOS
# =============================================================================

class VentanaCursos:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("📚 Gestión de Cursos")
        self.window.geometry("950x550")
        
        main_frame = tk.Frame(self.window, bg='#f5f5f5')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="📚 GESTIÓN DE CURSOS",
                font=('Helvetica', 14, 'bold'), bg='#f5f5f5').pack(pady=10)
        
        btn_frame = tk.Frame(main_frame, bg='#f5f5f5')
        btn_frame.pack(fill='x', pady=5)
        
        tk.Button(btn_frame, text="➕ Nuevo Curso", command=self.nuevo_curso,
                  bg='#4caf50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_datos,
                  bg='#2196f3', fg='white').pack(side='left', padx=5)
        
        columns = ('ID', 'Código', 'Nombre', 'Modalidad', 'Inicio', 'Fin', 'Inversión', 'Estado')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=18)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80 if col not in ['Nombre', 'Código'] else 100)
        
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.cargar_datos()
    
    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for cur in listar_cursos():
            self.tree.insert('', 'end', values=(
                cur['id_curso'], cur['codigo'], cur['nombre'], cur['modalidad'],
                cur['fecha_inicio'], cur['fecha_fin'], f"${cur['inversion']}", cur['estado']
            ))
    
    def nuevo_curso(self):
        form = FormularioCurso(self.window)
        if form.result:
            self.cargar_datos()


class FormularioCurso:
    def __init__(self, parent):
        self.result = None
        self.window = tk.Toplevel(parent)
        self.window.title("➕ Nuevo Curso")
        self.window.geometry("450x450")
        self.window.transient(parent)
        self.window.grab_set()
        
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        fields = [
            ('código', 'Código:'),
            ('nombre', 'Nombre:'),
            ('modalidad', 'Modalidad:'),
            ('inicio', 'Fecha Inicio (YYYY-MM-DD):'),
            ('fin', 'Fecha Fin (YYYY-MM-DD):'),
            ('hora_inicio', 'Hora Inicio (HH:MM):'),
            ('hora_fin', 'Hora Fin (HH:MM):'),
            ('días', 'Días (ej: Lunes,Miércoles):'),
            ('inversión', 'Inversión:'),
        ]
        
        self.entries = {}
        
        for i, (key, label) in enumerate(fields):
            tk.Label(main_frame, text=label).grid(row=i, column=0, sticky='w', pady=3)
            entry = tk.Entry(main_frame, width=30)
            entry.grid(row=i, column=1, pady=3, padx=5)
            self.entries[key] = entry
        
        # Valores por defecto
        self.entries['inversión'].insert(0, '150.0')
        self.entries['hora_inicio'].insert(0, '19:00')
        self.entries['hora_fin'].insert(0, '21:00')
        self.entries['días'].insert(0, 'Lunes,Miércoles,Viernes')
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=len(fields), columnspan=2, pady=15)
        
        tk.Button(btn_frame, text="✅ Guardar", command=self.guardar,
                  bg='#4caf50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=self.window.destroy,
                  bg='#f44336', fg='white').pack(side='left', padx=5)
    
    def guardar(self):
        datos = {k: v.get().strip() for k, v in self.entries.items()}
        
        if not datos['código'] or not datos['nombre']:
            messagebox.showerror("Error", "Código y nombre son requeridos")
            return
        
        try:
            inversion = float(datos['inversión'])
        except ValueError:
            inversion = 150.0
        
        result = registrar_curso(
            codigo=datos['código'],
            nombre=datos['nombre'],
            modalidad='Online',
            fecha_inicio=datos['inicio'],
            fecha_fin=datos['fin'],
            horario_inicio=datos['hora_inicio'],
            horario_fin=datos['hora_fin'],
            dias_semana=datos['días'],
            inversion=inversion
        )
        
        if result['exito']:
            messagebox.showinfo("Éxito", result['mensaje'])
            self.result = True
            self.window.destroy()
        else:
            messagebox.showerror("Error", result['error'])


# =============================================================================
# VENTANA: INSCRIPCIONES
# =============================================================================

class VentanaInscripciones:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("📝 Gestión de Inscripciones")
        self.window.geometry("950x550")
        
        main_frame = tk.Frame(self.window, bg='#f5f5f5')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="📝 GESTIÓN DE INSCRIPCIONES",
                font=('Helvetica', 14, 'bold'), bg='#f5f5f5').pack(pady=10)
        
        btn_frame = tk.Frame(main_frame, bg='#f5f5f5')
        btn_frame.pack(fill='x', pady=5)
        
        tk.Button(btn_frame, text="➕ Nueva Inscripción", command=self.nueva_inscripcion,
                  bg='#4caf50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_datos,
                  bg='#2196f3', fg='white').pack(side='left', padx=5)
        
        columns = ('ID', 'Estudiante', 'Cédula', 'Curso', 'Fecha', 'PDF', 'Pago', 'Estado')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=18)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80 if col not in ['Estudiante', 'Curso'] else 150)
        
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.cargar_datos()
    
    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for ins in listar_inscripciones():
            self.tree.insert('', 'end', values=(
                ins['id_inscripcion'], ins['nombre_estudiante'], ins['identificacion'],
                ins['nombre_curso'], str(ins['fecha_inscripcion'])[:10] if ins['fecha_inscripcion'] else '',
                '✅' if ins['tiene_pdf_cedula'] else '❌',
                '✅' if ins['tiene_pago'] else '❌',
                ins['estado']
            ))
    
    def nueva_inscripcion(self):
        form = FormularioInscripcion(self.window)
        if form.result:
            self.cargar_datos()


class FormularioInscripcion:
    def __init__(self, parent):
        self.result = None
        self.window = tk.Toplevel(parent)
        self.window.title("➕ Nueva Inscripción")
        self.window.geometry("400x250")
        self.window.transient(parent)
        self.window.grab_set()
        
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Seleccionar estudiante
        tk.Label(main_frame, text="Estudiante:").grid(row=0, column=0, sticky='w', pady=5)
        self.estudiante_combo = ttk.Combobox(main_frame, width=30)
        estudiantes = listar_estudiantes()
        self.estudiante_combo['values'] = [f"{e['nombres_completos']} ({e['identificacion']})" for e in estudiantes]
        self.estudiante_combo.grid(row=0, column=1, pady=5)
        
        # Seleccionar curso
        tk.Label(main_frame, text="Curso:").grid(row=1, column=0, sticky='w', pady=5)
        self.curso_combo = ttk.Combobox(main_frame, width=30)
        cursos = listar_cursos(estado='activo')
        self.curso_combo['values'] = [f"{c['nombre']} ({c['codigo']})" for c in cursos]
        self.curso_combo.grid(row=1, column=1, pady=5)
        
        # Checkboxes
        self.pdf_var = tk.BooleanVar(value=True)
        tk.Checkbutton(main_frame, text="Tiene copia de cédula en PDF", variable=self.pdf_var).grid(row=2, columnspan=2, pady=10)
        
        self.pago_var = tk.BooleanVar(value=True)
        tk.Checkbutton(main_frame, text="Tiene comprobante de pago", variable=self.pago_var).grid(row=3, columnspan=2, pady=10)
        
        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=4, columnspan=2, pady=15)
        
        tk.Button(btn_frame, text="✅ Inscribir", command=self.guardar,
                  bg='#4caf50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=self.window.destroy,
                  bg='#f44336', fg='white').pack(side='left', padx=5)
    
    def guardar(self):
        est_idx = self.estudiante_combo.current()
        cur_idx = self.curso_combo.current()
        
        if est_idx < 0 or cur_idx < 0:
            messagebox.showerror("Error", "Seleccione estudiante y curso")
            return
        
        estudiantes = listar_estudiantes()
        cursos = listar_cursos(estado='activo')
        
        result = inscribir_estudiante(
            id_estudiante=estudiantes[est_idx]['id_estudiante'],
            id_curso=cursos[cur_idx]['id_curso'],
            tiene_pdf_cedula=self.pdf_var.get(),
            tiene_pago=self.pago_var.get()
        )
        
        if result['exito']:
            messagebox.showinfo("Éxito", result['mensaje'])
            self.result = True
            self.window.destroy()
        else:
            messagebox.showerror("Error", result['error'])


# =============================================================================
# VENTANA: CERTIFICADOS
# =============================================================================

class VentanaCertificados:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("🏆 Gestión de Certificados")
        self.window.geometry("950x550")
        
        main_frame = tk.Frame(self.window, bg='#f5f5f5')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="🏆 GESTIÓN DE CERTIFICADOS",
                font=('Helvetica', 14, 'bold'), bg='#f5f5f5').pack(pady=10)
        
        btn_frame = tk.Frame(main_frame, bg='#f5f5f5')
        btn_frame.pack(fill='x', pady=5)
        
        tk.Button(btn_frame, text="➕ Generar Certificado", command=self.generar_certificado,
                  bg='#4caf50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_datos,
                  bg='#2196f3', fg='white').pack(side='left', padx=5)
        
        columns = ('ID', 'Estudiante', 'Cédula', 'Curso', 'N° Certificado', 'Fecha', 'Estado', 'Calif.')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=18)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80 if col not in ['Estudiante', 'Curso', 'N° Certificado'] else 130)
        
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.cargar_datos()
    
    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for cert in listar_certificaciones():
            self.tree.insert('', 'end', values=(
                cert['id_certificacion'], cert['nombre_estudiante'], cert['identificacion'],
                cert['nombre_curso'], cert['numero_certificado'],
                str(cert['fecha_emision'])[:10] if cert['fecha_emision'] else '',
                cert['estado'], cert['calificacion'] or '-'
            ))
    
    def generar_certificado(self):
        form = FormularioCertificado(self.window)
        if form.result:
            self.cargar_datos()


class FormularioCertificado:
    def __init__(self, parent):
        self.result = None
        self.window = tk.Toplevel(parent)
        self.window.title("➕ Generar Certificado")
        self.window.geometry("350x200")
        self.window.transient(parent)
        self.window.grab_set()
        
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        tk.Label(main_frame, text="Inscripción:").grid(row=0, column=0, sticky='w', pady=5)
        self.inscripcion_combo = ttk.Combobox(main_frame, width=30)
        inscripciones = listar_inscripciones(estado='inscrito')
        self.inscripcion_combo['values'] = [f"{i['nombre_estudiante']} - {i['nombre_curso']}" for i in inscripciones]
        self.inscripcion_combo.grid(row=0, column=1, pady=5)
        
        tk.Label(main_frame, text="Calificación (0-100):").grid(row=1, column=0, sticky='w', pady=5)
        self.calif_spin = tk.Spinbox(main_frame, from_=0, to=100, width=28)
        self.calif_spin.set(80)
        self.calif_spin.grid(row=1, column=1, pady=5)
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=2, columnspan=2, pady=15)
        
        tk.Button(btn_frame, text="✅ Generar", command=self.guardar,
                  bg='#4caf50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=self.window.destroy,
                  bg='#f44336', fg='white').pack(side='left', padx=5)
    
    def guardar(self):
        idx = self.inscripcion_combo.current()
        if idx < 0:
            messagebox.showerror("Error", "Seleccione una inscripción")
            return
        
        try:
            calif = float(self.calif_spin.get())
        except ValueError:
            messagebox.showerror("Error", "Calificación inválida")
            return
        
        inscripciones = listar_inscripciones(estado='inscrito')
        result = generar_certificado(
            id_inscripcion=inscripciones[idx]['id_inscripcion'],
            calificacion=calif
        )
        
        if result['exito']:
            messagebox.showinfo("Éxito", f"{result['mensaje']}\n\nCertificado: {result['numero_certificado']}\nPDF: {result['pdf_path']}")
            self.result = True
            self.window.destroy()
        else:
            messagebox.showerror("Error", result['error'])


# =============================================================================
# VENTANA: REPORTES
# =============================================================================

class VentanaReportes:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("📊 Reportes y Estadísticas")
        self.window.geometry("700x500")
        
        main_frame = tk.Frame(self.window, bg='#f5f5f5')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="📊 ESTADÍSTICAS DEL SISTEMA",
                font=('Helvetica', 16, 'bold'), bg='#f5f5f5').pack(pady=10)
        
        # Frame de estadísticas
        stats_frame = tk.LabelFrame(main_frame, text="Resumen General", font=('Helvetica', 11, 'bold'), padx=10, pady=10)
        stats_frame.pack(fill='x', pady=10)
        
        self.stats_text = tk.Text(stats_frame, height=8, width=60, font=('Courier', 10), bg='white')
        self.stats_text.pack(fill='x')
        
        tk.Button(main_frame, text="🔄 Actualizar", command=self.cargar_estadisticas,
                  bg='#2196f3', fg='white', font=('Helvetica', 10)).pack(pady=10)
        
        # Cursos populares
        cursos_frame = tk.LabelFrame(main_frame, text="Cursos con más inscripciones", font=('Helvetica', 11, 'bold'), padx=10, pady=10)
        cursos_frame.pack(fill='x', pady=10)
        
        self.cursos_text = tk.Text(cursos_frame, height=5, width=60, font=('Courier', 10), bg='white')
        self.cursos_text.pack(fill='x')
        
        self.cargar_estadisticas()
    
    def cargar_estadisticas(self):
        stats = obtener_estadisticas()
        
        texto = f"""
   Total Estudiantes:     {stats['total_estudiantes']}
   Total Docentes:       {stats['total_docentes']}
   Total Cursos:         {stats['total_cursos']}
   Total Inscripciones:  {stats['total_inscripciones']}
   Certificados:         {stats['total_certificados']}
        """
        self.stats_text.delete('1.0', 'end')
        self.stats_text.insert('1.0', texto)
        
        cursos_texto = "   Curso                              Inscripciones\n"
        cursos_texto += "   " + "-" * 50 + "\n"
        for curso in stats['cursos_populares']:
            cursos_texto += f"   {curso['nombre'][:35]:<35} {curso['total']}\n"
        
        self.cursos_text.delete('1.0', 'end')
        self.cursos_text.insert('1.0', cursos_texto)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

def main():
    """Función principal."""
    root = tk.Tk()
    app = ABACOMGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()