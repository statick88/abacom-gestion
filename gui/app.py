"""
================================================================================
INTERFAZ GRAFICA CON TKINTER - SISTEMA DE GESTIÓN EDUCATIVA ABACOM
================================================================================
Aplicación de escritorio usando tkinter con diseño profesional estilo Linear.
Modular, minimalista, moderno e intuitivo.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

import sys
import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional, List, Dict, Callable
from datetime import datetime

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
    buscar_cursos,
    iniciar_sesion,
    registrar_usuario,
    validar_email_formato
)


# =============================================================================
# DISEÑO - ESTILO LINEAR (Ultra-minimal, Purple accent, Precise)
# =============================================================================

class LinearDesign:
    """Sistema de diseño profesional estilo Linear - Ultra minimal."""
    
    # Paleta de colores
    COLORS = {
        # Backgrounds
        'bg_app': '#0F0F12',           # Fondo oscuro principal (Linear dark)
        'bg_surface': '#16161A',      # Superficie de tarjetas
        'bg_elevated': '#1E1E24',     # Elementos elevados
        'bg_input': '#242429',         # Background inputs
        
        # Texto
        'text_primary': '#FFFFFE',     # Texto principal (blanco)
        'text_secondary': '#9B9B9B',   # Texto secundario
        'text_muted': '#5C5C66',       # Texto muted
        
        # Accent - Linear purple
        'accent': '#5E6AD2',          # Purple principal
        'accent_hover': '#7178E8',     # Purple hover
        'accent_pressed': '#4A55B8',  # Purple pressed
        
        # Estados
        'success': '#4ADE80',         # Verde brillante
        'warning': '#FBBF24',         # Amarillo
        'danger': '#F87171',          # Rojo
        'info': '#60A5FA',            # Azul
        
        # Borders
        'border': '#2E2E36',           # Borde default
        'border_focus': '#5E6AD2',     # Borde focus
    }
    
    # Espaciado (4px grid)
    SPACE = {
        'xs': 4,
        'sm': 8,
        'md': 12,
        'lg': 16,
        'xl': 24,
        '2xl': 32,
    }
    
    # Border radius
    RADIUS = {
        'sm': 4,
        'md': 6,
        'lg': 8,
        'xl': 12,
    }
    
    # Fonts (tkinter solo soporta normal/bold, no semibold)
    FONTS = {
        'title': ('Inter', 20, 'bold'),
        'heading': ('Inter', 16, 'bold'),
        'subhead': ('Inter', 14, 'bold'),
        'body': ('Inter', 13),
        'body_bold': ('Inter', 13, 'bold'),
        'small': ('Inter', 11),
        'mono': ('JetBrains Mono', 12),
    }


# =============================================================================
# WIDGETS CUSTOMIZADOS
# =============================================================================

class ModernButton(tk.Frame):
    """Botón moderno con estados."""
    
    def __init__(self, parent, text: str, command: Callable, 
                 variant: str = 'primary', size: str = 'md', **kwargs):
        super().__init__(parent, bg=LinearDesign.COLORS['bg_app'])
        
        self.command = command
        self.variant = variant
        self._hover = False
        self._pressed = False
        
        # Variants
        colors = {
            'primary': (LinearDesign.COLORS['accent'], LinearDesign.COLORS['accent_hover'], 
                       LinearDesign.COLORS['accent_pressed'], '#FFFFFF'),
            'secondary': (LinearDesign.COLORS['bg_elevated'], LinearDesign.COLORS['bg_input'],
                         LinearDesign.COLORS['border'], LinearDesign.COLORS['text_primary']),
            'success': (LinearDesign.COLORS['success'], '#3ECF73', '#22C55E', '#0F0F12'),
            'danger': (LinearDesign.COLORS['danger'], '#F98B8B', '#EF4444', '#FFFFFF'),
            'ghost': (LinearDesign.COLORS['bg_surface'], LinearDesign.COLORS['bg_elevated'], 
                     LinearDesign.COLORS['border'], LinearDesign.COLORS['text_secondary']),
        }
        
        bg, bg_hover, bg_pressed, fg = colors.get(variant, colors['primary'])
        
        # Size config
        sizes = {'sm': (8, 4), 'md': (12, 8), 'lg': (16, 12)}
        pady, padx = sizes.get(size, sizes['md'])
        
        self.btn = tk.Label(
            self, text=text, font=LinearDesign.FONTS['body_bold'],
            bg=bg, fg=fg, padx=padx, pady=pady,
            cursor='hand2', relief='flat',
            highlightthickness=0
        )
        self.btn.pack()
        
        # Store colors for hover
        self._colors = (bg, bg_hover, bg_pressed, fg)
        
        # Events
        self.btn.bind('<Enter>', self._on_enter)
        self.btn.bind('<Leave>', self._on_leave)
        self.btn.bind('<Button-1>', self._on_press)
        self.btn.bind('<ButtonRelease-1>', self._on_release)
        
        self.config(bg=LinearDesign.COLORS['bg_app'])
    
    def _on_enter(self, e):
        if self.variant != 'ghost':
            self.btn.config(bg=self._colors[1])
    
    def _on_leave(self, e):
        if self.variant != 'ghost':
            self.btn.config(bg=self._colors[0])
    
    def _on_press(self, e):
        if self.variant != 'ghost':
            self.btn.config(bg=self._colors[2])
        self.command()
    
    def _on_release(self, e):
        if self.variant != 'ghost':
            self.btn.config(bg=self._colors[1])


class SurfaceCard(tk.Frame):
    """Tarjeta con estilo de superficie elevada."""
    
    def __init__(self, parent, accent: bool = False, **kwargs):
        super().__init__(
            parent, 
            bg=LinearDesign.COLORS['bg_surface'],
            highlightthickness=1,
            highlightcolor=LinearDesign.COLORS['border'],
            highlightbackground=LinearDesign.COLORS['border'],
            relief='flat',
            bd=0,
            **kwargs
        )
        
        if accent:
            accent_bar = tk.Frame(self, bg=LinearDesign.COLORS['accent'], height=2)
            accent_bar.pack(fill='x')


class ModernEntry(tk.Frame):
    """Input moderno con borde."""
    
    def __init__(self, parent, width: int = 30, **kwargs):
        super().__init__(parent, bg=LinearDesign.COLORS['bg_app'])
        
        self.entry = tk.Entry(
            self,
            font=LinearDesign.FONTS['body'],
            bg=LinearDesign.COLORS['bg_input'],
            fg=LinearDesign.COLORS['text_primary'],
            insertbackground=LinearDesign.COLORS['accent'],
            relief='flat',
            bd=0,
            width=width,
            highlightthickness=1,
            highlightcolor=LinearDesign.COLORS['border'],
            highlightbackground=LinearDesign.COLORS['border'],
            **kwargs
        )
        self.entry.pack(padx=LinearDesign.SPACE['sm'], pady=LinearDesign.SPACE['xs'])
        
        # Focus effect
        self.entry.bind('<FocusIn>', lambda e: self.entry.config(
            highlightcolor=LinearDesign.COLORS['accent']))
        self.entry.bind('<FocusOut>', lambda e: self.entry.config(
            highlightcolor=LinearDesign.COLORS['border']))
    
    def get(self) -> str:
        return self.entry.get().strip()
    
    def set(self, value: str):
        self.entry.delete(0, 'end')
        self.entry.insert(0, value)


class ModernLabel(tk.Label):
    """Label con estilos predefinidos."""
    
    def __init__(self, parent, text: str, style: str = 'body', **kwargs):
        super().__init__(
            parent, text=text,
            font=LinearDesign.FONTS.get(style, LinearDesign.FONTS['body']),
            fg=LinearDesign.COLORS['text_primary'],
            bg=LinearDesign.COLORS['bg_surface'] if 'bg' not in kwargs else kwargs.get('bg'),
            **kwargs
        )


class ModernModal(tk.Toplevel):
    """Ventana modal moderna."""
    
    def __init__(self, parent, title: str, size: str = "450x400"):
        super().__init__(parent)
        
        self.title(title)
        self.geometry(size)
        self.configure(bg=LinearDesign.COLORS['bg_app'])
        
        # Modal setup
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        # Prevent closing without grab
        self.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _on_close(self):
        self.grab_release()
        self.destroy()


# =============================================================================
# PANTALLA DE LOGIN
# =============================================================================

class LoginScreen:
    """Pantalla de inicio de sesión."""
    
    def __init__(self, on_login_success):
        self.on_login_success = on_login_success
        
        self.root = tk.Tk()
        self.root.title("ABACOM - Iniciar Sesión")
        self.root.geometry("450x500")
        self.root.resizable(False, False)
        self.root.configure(bg=LinearDesign.COLORS['bg_app'])
        
        self._build_ui()
    
    def _build_ui(self):
        """Construye la interfaz de login."""
        # Container principal
        container = tk.Frame(self.root, bg=LinearDesign.COLORS['bg_app'])
        container.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Logo/Icono
        tk.Label(container, text="◈", font=('Segoe UI Emoji', 48),
                bg=LinearDesign.COLORS['bg_app'],
                fg=LinearDesign.COLORS['accent']).pack(pady=(20, 10))
        
        # Título
        tk.Label(container, text="ABACOM",
                font=LinearDesign.FONTS['title'],
                fg=LinearDesign.COLORS['text_primary'],
                bg=LinearDesign.COLORS['bg_app']).pack()
        
        tk.Label(container, text="Sistema de Gestión Educativa",
                font=LinearDesign.FONTS['small'],
                fg=LinearDesign.COLORS['text_secondary'],
                bg=LinearDesign.COLORS['bg_app']).pack(pady=(0, 30))
        
        # Formulario
        form_frame = tk.Frame(container, bg=LinearDesign.COLORS['bg_app'])
        form_frame.pack(fill='x')
        
        # Usuario/Email
        tk.Label(form_frame, text="Usuario o Email",
                font=LinearDesign.FONTS['body'],
                fg=LinearDesign.COLORS['text_secondary'],
                bg=LinearDesign.COLORS['bg_app']).pack(anchor='w')
        
        self.entry_user = tk.Entry(form_frame, font=LinearDesign.FONTS['body'],
                                   bg=LinearDesign.COLORS['bg_input'],
                                   fg=LinearDesign.COLORS['text_primary'],
                                   insertbackground=LinearDesign.COLORS['accent'],
                                   relief='flat', width=35,
                                   highlightthickness=1,
                                   highlightcolor=LinearDesign.COLORS['border'],
                                   highlightbackground=LinearDesign.COLORS['border'])
        self.entry_user.pack(pady=(4, 16))
        
        # Contraseña
        tk.Label(form_frame, text="Contraseña",
                font=LinearDesign.FONTS['body'],
                fg=LinearDesign.COLORS['text_secondary'],
                bg=LinearDesign.COLORS['bg_app']).pack(anchor='w')
        
        self.entry_pass = tk.Entry(form_frame, font=LinearDesign.FONTS['body'],
                                   bg=LinearDesign.COLORS['bg_input'],
                                   fg=LinearDesign.COLORS['text_primary'],
                                   insertbackground=LinearDesign.COLORS['accent'],
                                   relief='flat', width=35,
                                   show="●",
                                   highlightthickness=1,
                                   highlightcolor=LinearDesign.COLORS['border'],
                                   highlightbackground=LinearDesign.COLORS['border'])
        self.entry_pass.pack(pady=(4, 20))
        
        # Botón登录
        btn_login = tk.Label(form_frame, text="Iniciar Sesión",
                           font=LinearDesign.FONTS['body_bold'],
                           bg=LinearDesign.COLORS['accent'],
                           fg='#FFFFFF', padx=20, pady=10,
                           cursor='hand2', relief='flat')
        btn_login.pack(fill='x')
        btn_login.bind('<Enter>', lambda e: btn_login.config(bg=LinearDesign.COLORS['accent_hover']))
        btn_login.bind('<Leave>', lambda e: btn_login.config(bg=LinearDesign.COLORS['accent']))
        btn_login.bind('<Button-1>', lambda e: self._do_login())
        
        # Bind Enter key
        self.entry_pass.bind('<Return>', lambda e: self._do_login())
        
        # Registro link
        reg_frame = tk.Frame(container, bg=LinearDesign.COLORS['bg_app'])
        reg_frame.pack(pady=20)
        
        tk.Label(reg_frame, text="¿No tienes cuenta?",
                font=LinearDesign.FONTS['small'],
                fg=LinearDesign.COLORS['text_muted'],
                bg=LinearDesign.COLORS['bg_app']).pack(side='left')
        
        reg_link = tk.Label(reg_frame, text="Regístrate",
                           font=LinearDesign.FONTS['small'],
                           fg=LinearDesign.COLORS['accent'],
                           bg=LinearDesign.COLORS['bg_app'],
                           cursor='hand2')
        reg_link.pack(side='left', padx=4)
        reg_link.bind('<Button-1>', lambda e: self._show_register())
        
        # Version
        tk.Label(container, text="v1.0.0",
                font=LinearDesign.FONTS['small'],
                fg=LinearDesign.COLORS['text_muted'],
                bg=LinearDesign.COLORS['bg_app']).pack(side='bottom', pady=10)
    
    def _do_login(self):
        """Procesa el login."""
        usuario = self.entry_user.get().strip()
        password = self.entry_pass.get()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Ingrese usuario y contraseña")
            return
        
        result = iniciar_sesion(usuario, password)
        
        if result['exito']:
            self.root.destroy()
            self.on_login_success(result['usuario'])
        else:
            messagebox.showerror("Error", result['error'])
    
    def _show_register(self):
        """Muestra formulario de registro."""
        reg = RegistrationModal(self.root, on_success=lambda msg: messagebox.showinfo("Éxito", msg))
    
    def run(self):
        """Inicia el loop de la pantalla de login."""
        self.root.mainloop()


class RegistrationModal(ModernModal):
    """Modal de registro de nuevos usuarios."""
    
    def __init__(self, parent, on_success):
        super().__init__(parent, "Crear Cuenta", "420x480")
        self.on_success = on_success
        
        inner = tk.Frame(self, bg=LinearDesign.COLORS['bg_surface'],
                        padx=LinearDesign.SPACE['xl'], pady=LinearDesign.SPACE['xl'])
        inner.pack(fill='both', expand=True)
        
        # Campos
        fields = [
            ('usuario', 'Usuario *'),
            ('nombres', 'Nombres Completos *'),
            ('email', 'Correo Electrónico *'),
            ('password', 'Contraseña *'),
            ('password2', 'Confirmar Contraseña *'),
        ]
        
        self.entries = {}
        
        for key, label in fields:
            tk.Label(inner, text=label, font=LinearDesign.FONTS['body'],
                    fg=LinearDesign.COLORS['text_secondary'],
                    bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w', pady=(LinearDesign.SPACE['md'], 4))
            
            entry = tk.Entry(inner, font=LinearDesign.FONTS['body'],
                           bg=LinearDesign.COLORS['bg_input'],
                           fg=LinearDesign.COLORS['text_primary'],
                           insertbackground=LinearDesign.COLORS['accent'],
                           relief='flat', width=35,
                           show="●" if 'password' in key else "",
                           highlightthickness=1,
                           highlightcolor=LinearDesign.COLORS['border'],
                           highlightbackground=LinearDesign.COLORS['border'])
            entry.pack(fill='x')
            self.entries[key] = entry
        
        # Info
        tk.Label(inner, text="Mínimo 8 caracteres para la contraseña",
                font=LinearDesign.FONTS['small'],
                fg=LinearDesign.COLORS['text_muted'],
                bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w', pady=(LinearDesign.SPACE['sm'], 0))
        
        # Botones
        btn_frame = tk.Frame(inner, bg=LinearDesign.COLORS['bg_surface'])
        btn_frame.pack(pady=LinearDesign.SPACE['xl'], fill='x')
        
        ModernButton(btn_frame, "Registrarse", self._do_register,
                    variant='primary').pack(side='left', padx=4)
        ModernButton(btn_frame, "Cancelar", self.destroy,
                    variant='ghost').pack(side='left', padx=4)
    
    def _do_register(self):
        """Procesa el registro."""
        datos = {k: v.get().strip() for k, v in self.entries.items()}
        
        # Validaciones
        if not all([datos['usuario'], datos['nombres'], datos['email'], datos['password']]):
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return
        
        if datos['password'] != datos['password2']:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        if len(datos['password']) < 8:
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres")
            return
        
        if not validar_email_formato(datos['email']):
            messagebox.showerror("Error", "Formato de correo electrónico inválido")
            return
        
        result = registrar_usuario(
            usuario=datos['usuario'],
            email=datos['email'],
            password=datos['password'],
            nombres=datos['nombres'],
            rol='estudiante'
        )
        
        if result['exito']:
            self.on_success(result['mensaje'])
            self.destroy()
        else:
            messagebox.showerror("Error", result['error'])


# =============================================================================
# APLICACIÓN PRINCIPAL
# =============================================================================

class ABACOMApp:
    """Aplicación principal con diseño Linear oscuro."""
    
    def __init__(self, usuario=None):
        self.usuario = usuario  # Usuario logueado
        
        self.root = tk.Tk()
        self.root.title("ABACOM - Sistema de Gestión")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg=LinearDesign.COLORS['bg_app'])
        
        # State
        self.current_view = None
        
        # Build UI
        self.build_header()
        self.build_navigation()
        self.build_content()
        self.build_status()
        
        # Load initial view
        self.show_estadisticas()
    
    def build_header(self):
        """Header con logo y título."""
        header = tk.Frame(self.root, bg=LinearDesign.COLORS['bg_surface'], height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Logo
        tk.Label(header, text="◈", font=('Segoe UI Emoji', 28),
                bg=LinearDesign.COLORS['bg_surface'],
                fg=LinearDesign.COLORS['accent']).pack(side='left', padx=LinearDesign.SPACE['lg'])
        
        # Title
        title_frame = tk.Frame(header, bg=LinearDesign.COLORS['bg_surface'])
        title_frame.pack(side='left', fill='y', pady=12)
        
        tk.Label(title_frame, text="ABACOM", font=LinearDesign.FONTS['heading'],
                fg=LinearDesign.COLORS['text_primary'],
                bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w')
        
        tk.Label(title_frame, text="Sistema de Gestión Educativa",
                font=LinearDesign.FONTS['small'],
                fg=LinearDesign.COLORS['text_muted'],
                bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w')
        
        # Date/Time
        self.datetime_label = tk.Label(header, text="",
                font=LinearDesign.FONTS['small'],
                fg=LinearDesign.COLORS['text_secondary'],
                bg=LinearDesign.COLORS['bg_surface'])
        self.datetime_label.pack(side='right', padx=LinearDesign.SPACE['lg'])
        
        self._update_datetime()
    
    def _update_datetime(self):
        """Actualiza la fecha/hora."""
        now = datetime.now().strftime("%d %b %Y • %H:%M")
        self.datetime_label.config(text=now)
        self.root.after(60000, self._update_datetime)
    
    def build_navigation(self):
        """Barra de navegación lateral."""
        nav = tk.Frame(self.root, bg=LinearDesign.COLORS['bg_surface'], width=220)
        nav.pack(side='left', fill='y')
        nav.pack_propagate(False)
        
        # Menu items
        menu_items = [
            ("📊", "Estadísticas", self.show_estadisticas),
            ("👨‍🎓", "Estudiantes", self.show_estudiantes),
            ("👨‍🏫", "Docentes", self.show_docentes),
            ("📚", "Cursos", self.show_cursos),
            ("📝", "Inscripciones", self.show_inscripciones),
            ("🏆", "Certificados", self.show_certificados),
            ("🔧", "Configuración", self.show_settings),
        ]
        
        for icon, label, command in menu_items:
            self._nav_item(nav, icon, label, command)
    
    def _nav_item(self, parent, icon: str, label: str, command: Callable):
        """Crea item de navegación."""
        nav_bg = LinearDesign.COLORS['bg_surface']
        item = tk.Frame(parent, bg=nav_bg, cursor='hand2')
        item.pack(fill='x', padx=LinearDesign.SPACE['sm'], pady=2)
        
        def on_enter(e): item.config(bg=LinearDesign.COLORS['bg_elevated'])
        def on_leave(e): item.config(bg=nav_bg)
        
        item.bind('<Enter>', on_enter)
        item.bind('<Leave>', on_leave)
        item.bind('<Button-1>', lambda e: command())
        
        tk.Label(item, text=icon, font=('Segoe UI Emoji', 14),
                bg=nav_bg, fg=LinearDesign.COLORS['text_secondary'],
                width=3).pack(side='left', pady=8)
        
        tk.Label(item, text=label, font=LinearDesign.FONTS['body'],
                bg=nav_bg, fg=LinearDesign.COLORS['text_primary']).pack(side='left')
    
    def build_content(self):
        """Área de contenido principal."""
        self.content_frame = tk.Frame(self.root, bg=LinearDesign.COLORS['bg_app'])
        self.content_frame.pack(side='left', fill='both', expand=True, 
                               padx=LinearDesign.SPACE['lg'], pady=LinearDesign.SPACE['lg'])
    
    def build_status(self):
        """Barra de estado inferior."""
        status = tk.Frame(self.root, bg=LinearDesign.COLORS['bg_surface'], height=28)
        status.pack(fill='x', side='bottom')
        status.pack_propagate(False)
        
        tk.Label(status, text="● Sistema listo", font=LinearDesign.FONTS['small'],
                fg=LinearDesign.COLORS['success'],
                bg=LinearDesign.COLORS['bg_surface']).pack(side='left', padx=LinearDesign.SPACE['lg'])
        
        tk.Label(status, text="v1.0.0", font=LinearDesign.FONTS['small'],
                fg=LinearDesign.COLORS['text_muted'],
                bg=LinearDesign.COLORS['bg_surface']).pack(side='right', padx=LinearDesign.SPACE['lg'])
    
    def clear_content(self):
        """Limpia el contenido."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    # =========================================================================
    # VISTAS
    # =========================================================================
    
    def show_estadisticas(self):
        """Vista de estadísticas."""
        self.clear_content()
        
        # Title
        title = tk.Label(self.content_frame, text="📊 Estadísticas",
                        font=LinearDesign.FONTS['title'],
                        fg=LinearDesign.COLORS['text_primary'],
                        bg=LinearDesign.COLORS['bg_app'])
        title.pack(anchor='w', pady=(0, LinearDesign.SPACE['lg']))
        
        # Stats grid
        stats = obtener_estadisticas()
        
        stat_cards = [
            ("Estudiantes", stats['total_estudiantes'], "👨‍🎓"),
            ("Docentes", stats['total_docentes'], "👨‍🏫"),
            ("Cursos", stats['total_cursos'], "📚"),
            ("Inscripciones", stats['total_inscripciones'], "📝"),
            ("Certificados", stats['total_certificados'], "🏆"),
        ]
        
        grid = tk.Frame(self.content_frame, bg=LinearDesign.COLORS['bg_app'])
        grid.pack(fill='x')
        
        for i, (label, value, icon) in enumerate(stat_cards):
            card = SurfaceCard(grid, accent=True)
            card.pack(side='left', padx=LinearDesign.SPACE['sm'], pady=LinearDesign.SPACE['sm'], fill='both', expand=True)
            
            inner = tk.Frame(card, bg=LinearDesign.COLORS['bg_surface'],
                           padx=LinearDesign.SPACE['lg'], pady=LinearDesign.SPACE['lg'])
            inner.pack(fill='both', expand=True)
            
            tk.Label(inner, text=icon, font=('Segoe UI Emoji', 24),
                    bg=LinearDesign.COLORS['bg_surface']).pack()
            
            tk.Label(inner, text=str(value), font=LinearDesign.FONTS['title'],
                    fg=LinearDesign.COLORS['text_primary'],
                    bg=LinearDesign.COLORS['bg_surface']).pack(pady=LinearDesign.SPACE['sm'])
            
            tk.Label(inner, text=label, font=LinearDesign.FONTS['small'],
                    fg=LinearDesign.COLORS['text_secondary'],
                    bg=LinearDesign.COLORS['bg_surface']).pack()
        
        # Cursos populares
        card = SurfaceCard(self.content_frame)
        card.pack(fill='x', pady=(LinearDesign.SPACE['lg'], 0))
        
        inner = tk.Frame(card, bg=LinearDesign.COLORS['bg_surface'],
                        padx=LinearDesign.SPACE['lg'], pady=LinearDesign.SPACE['md'])
        inner.pack(fill='x')
        
        tk.Label(inner, text="Cursos con más inscripciones",
                font=LinearDesign.FONTS['subhead'],
                fg=LinearDesign.COLORS['text_primary'],
                bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w', pady=(0, LinearDesign.SPACE['md']))
        
        for curso in stats.get('cursos_populares', [])[:5]:
            row = tk.Frame(inner, bg=LinearDesign.COLORS['bg_surface'])
            row.pack(fill='x', pady=4)
            
            tk.Label(row, text=curso['nombre'], font=LinearDesign.FONTS['body'],
                    fg=LinearDesign.COLORS['text_primary'],
                    bg=LinearDesign.COLORS['bg_surface']).pack(side='left')
            
            tk.Label(row, text=f"{curso['total']} ins.", font=LinearDesign.FONTS['small'],
                    fg=LinearDesign.COLORS['accent'],
                    bg=LinearDesign.COLORS['bg_surface']).pack(side='right')
    
    def show_estudiantes(self):
        """Vista de estudiantes."""
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=LinearDesign.COLORS['bg_app'])
        header.pack(fill='x', pady=(0, LinearDesign.SPACE['lg']))
        
        tk.Label(header, text="👨‍🎓 Gestión de Estudiantes",
                font=LinearDesign.FONTS['title'],
                fg=LinearDesign.COLORS['text_primary'],
                bg=LinearDesign.COLORS['bg_app']).pack(side='left')
        
        btn_frame = tk.Frame(header, bg=LinearDesign.COLORS['bg_app'])
        btn_frame.pack(side='right')
        
        ModernButton(btn_frame, "+ Nuevo", lambda: self._form_estudiante(), 
                    variant='primary', size='md').pack(side='left', padx=4)
        ModernButton(btn_frame, "🔍 Buscar", self._buscar_estudiante,
                    variant='secondary', size='md').pack(side='left', padx=4)
        
        # Table
        self._build_table(['ID', 'Cédula', 'Nombres', 'Teléfono', 'Celular', 'Correo', 'Estado'],
                         lambda: listar_estudiantes())
    
    def show_docentes(self):
        """Vista de docentes."""
        self.clear_content()
        
        header = tk.Frame(self.content_frame, bg=LinearDesign.COLORS['bg_app'])
        header.pack(fill='x', pady=(0, LinearDesign.SPACE['lg']))
        
        tk.Label(header, text="👨‍🏫 Gestión de Docentes",
                font=LinearDesign.FONTS['title'],
                fg=LinearDesign.COLORS['text_primary'],
                bg=LinearDesign.COLORS['bg_app']).pack(side='left')
        
        ModernButton(header, "+ Nuevo", lambda: self._form_docente(),
                    variant='primary', size='md').pack(side='right')
        
        self._build_table(['ID', 'Nombres', 'Teléfono', 'Celular', 'Correo', 'Especialización', 'Estado'],
                         lambda: listar_docentes())
    
    def show_cursos(self):
        """Vista de cursos."""
        self.clear_content()
        
        header = tk.Frame(self.content_frame, bg=LinearDesign.COLORS['bg_app'])
        header.pack(fill='x', pady=(0, LinearDesign.SPACE['lg']))
        
        tk.Label(header, text="📚 Gestión de Cursos",
                font=LinearDesign.FONTS['title'],
                fg=LinearDesign.COLORS['text_primary'],
                bg=LinearDesign.COLORS['bg_app']).pack(side='left')
        
        ModernButton(header, "+ Nuevo", lambda: self._form_curso(),
                    variant='primary', size='md').pack(side='right')
        
        self._build_table(['ID', 'Código', 'Nombre', 'Modalidad', 'Inicio', 'Fin', 'Inversión', 'Estado'],
                         lambda: listar_cursos())
    
    def show_inscripciones(self):
        """Vista de inscripciones."""
        self.clear_content()
        
        header = tk.Frame(self.content_frame, bg=LinearDesign.COLORS['bg_app'])
        header.pack(fill='x', pady=(0, LinearDesign.SPACE['lg']))
        
        tk.Label(header, text="📝 Inscripciones",
                font=LinearDesign.FONTS['title'],
                fg=LinearDesign.COLORS['text_primary'],
                bg=LinearDesign.COLORS['bg_app']).pack(side='left')
        
        ModernButton(header, "+ Nueva", lambda: self._form_inscripcion(),
                    variant='primary', size='md').pack(side='right')
        
        self._build_table(['Estudiante', 'Cédula', 'Curso', 'Fecha', 'PDF', 'Pago', 'Estado'],
                         lambda: self._format_inscripciones())
    
    def show_certificados(self):
        """Vista de certificados."""
        self.clear_content()
        
        header = tk.Frame(self.content_frame, bg=LinearDesign.COLORS['bg_app'])
        header.pack(fill='x', pady=(0, LinearDesign.SPACE['lg']))
        
        tk.Label(header, text="🏆 Certificados",
                font=LinearDesign.FONTS['title'],
                fg=LinearDesign.COLORS['text_primary'],
                bg=LinearDesign.COLORS['bg_app']).pack(side='left')
        
        ModernButton(header, "+ Generar", lambda: self._form_certificado(),
                    variant='primary', size='md').pack(side='right')
        
        self._build_table(['Estudiante', 'Cédula', 'Curso', 'N° Cert', 'Fecha', 'Estado', 'Calif'],
                         lambda: self._format_certificados())
    
    def show_settings(self):
        """Vista de configuración."""
        self.clear_content()
        
        tk.Label(self.content_frame, text="🔧 Configuración",
                font=LinearDesign.FONTS['title'],
                fg=LinearDesign.COLORS['text_primary'],
                bg=LinearDesign.COLORS['bg_app']).pack(anchor='w', pady=(0, LinearDesign.SPACE['lg']))
        
        card = SurfaceCard(self.content_frame)
        card.pack(fill='x')
        
        inner = tk.Frame(card, bg=LinearDesign.COLORS['bg_surface'],
                        padx=LinearDesign.SPACE['lg'], pady=LinearDesign.SPACE['lg'])
        inner.pack(fill='x')
        
        tk.Label(inner, text="Acerca de ABACOM", font=LinearDesign.FONTS['subhead'],
                fg=LinearDesign.COLORS['text_primary'],
                bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w')
        
        tk.Label(inner, text="Sistema de Gestión Educativa v1.0.0\nDesarrollado para ABACOM",
                font=LinearDesign.FONTS['body'],
                fg=LinearDesign.COLORS['text_secondary'],
                bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w', pady=LinearDesign.SPACE['sm'])
    
    # =========================================================================
    # HELPERS
    # =========================================================================
    
    def _build_table(self, columns: list, data_loader: Callable):
        """Construye tabla de datos."""
        # Container
        container = tk.Frame(self.content_frame, bg=LinearDesign.COLORS['border'], bd=1)
        container.pack(fill='both', expand=True)
        
        # Treeview
        tree = ttk.Treeview(container, columns=columns, show='headings',
                           style='Modern.Treeview')
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Modern.Treeview',
                       background=LinearDesign.COLORS['bg_surface'],
                       foreground=LinearDesign.COLORS['text_primary'],
                       font=LinearDesign.FONTS['body'],
                       rowheight=32,
                       fieldbackground=LinearDesign.COLORS['bg_surface'])
        style.configure('Modern.Treeview.Heading',
                       font=LinearDesign.FONTS['body_bold'],
                       background=LinearDesign.COLORS['bg_elevated'],
                       foreground=LinearDesign.COLORS['text_primary'])
        style.map('Modern.Treeview', background=[('selected', LinearDesign.COLORS['accent'])])
        
        # Columns
        for col in columns:
            tree.heading(col, text=col)
            width = 100 if col not in ['Nombres', 'Nombre', 'Curso', 'Correo'] else 150
            tree.column(col, width=width, minwidth=60)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load data
        try:
            for row in data_loader():
                tree.insert('', 'end', values=row)
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def _format_inscripciones(self):
        """Formatea inscripciones para tabla."""
        return [(ins['nombre_estudiante'], ins['identificacion'],
                ins['nombre_curso'], str(ins['fecha_inscripcion'])[:10] if ins['fecha_inscripcion'] else '',
                '✓' if ins['tiene_pdf_cedula'] else '✗',
                '✓' if ins['tiene_pago'] else '✗',
                ins['estado']) for ins in listar_inscripciones()]
    
    def _format_certificados(self):
        """Formatea certificados para tabla."""
        return [(cert['nombre_estudiante'], cert['identificacion'],
                cert['nombre_curso'], cert['numero_certificado'],
                str(cert['fecha_emision'])[:10] if cert['fecha_emision'] else '',
                cert['estado'], str(cert['calificacion']) if cert['calificacion'] else '—')
                for cert in listar_certificaciones()]
    
    # =========================================================================
    # FORMULARIOS (MODALES)
    # =========================================================================
    
    def _form_estudiante(self):
        """Formulario de estudiante como modal."""
        modal = ModernModal(self.root, "Nuevo Estudiante", "420x400")
        
        inner = tk.Frame(modal, bg=LinearDesign.COLORS['bg_surface'],
                        padx=LinearDesign.SPACE['xl'], pady=LinearDesign.SPACE['xl'])
        inner.pack(fill='both', expand=True)
        
        fields = [('cedula', 'Cédula *'), ('nombres', 'Nombres *'), 
                 ('telefono', 'Teléfono'), ('celular', 'Celular *'), 
                 ('correo', 'Correo *')]
        
        entries = {}
        
        for key, label in fields:
            tk.Label(inner, text=label, font=LinearDesign.FONTS['body'],
                    fg=LinearDesign.COLORS['text_secondary'],
                    bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w', pady=(LinearDesign.SPACE['md'], 4))
            
            entry = ModernEntry(inner, width=35)
            entry.pack(fill='x')
            entries[key] = entry
        
        # Buttons
        btn_frame = tk.Frame(inner, bg=LinearDesign.COLORS['bg_surface'])
        btn_frame.pack(pady=LinearDesign.SPACE['xl'], fill='x')
        
        ModernButton(btn_frame, "Guardar", lambda: self._save_estudiante(entries, modal),
                    variant='primary').pack(side='left', padx=4)
        ModernButton(btn_frame, "Cancelar", modal.destroy,
                    variant='ghost').pack(side='left', padx=4)
    
    def _save_estudiante(self, entries, modal):
        """Guarda estudiante desde formulario."""
        datos = {k: v.get() for k, v in entries.items()}
        
        if not datos['nombres'] or not datos['celular'] or not datos['correo']:
            messagebox.showerror("Error", "Campos requeridos")
            return
        
        if not validar_cedula_ecuador(datos['cedula']):
            messagebox.showerror("Error", "Cédula inválida")
            return
        
        result = registrar_estudiante(
            identificacion=datos['cedula'],
            nombres_completos=datos['nombres'],
            telefono_fijo=datos['telefono'] or None,
            celular=datos['celular'],
            correo_electronico=datos['correo']
        )
        
        if result['exito']:
            messagebox.showinfo("Éxito", result['mensaje'])
            modal.destroy()
            self.show_estudiantes()
        else:
            messagebox.showerror("Error", result['error'])
    
    def _buscar_estudiante(self):
        """Buscar estudiante."""
        texto = simpledialog.askstring("Buscar", "Nombre, cédula o correo:")
        if texto:
            self.clear_content()
            
            tk.Label(self.content_frame, text=f"🔍 Resultados: {texto}",
                    font=LinearDesign.FONTS['title'],
                    fg=LinearDesign.COLORS['text_primary'],
                    bg=LinearDesign.COLORS['bg_app']).pack(anchor='w', pady=(0, LinearDesign.SPACE['lg']))
            
            self._build_table(['ID', 'Cédula', 'Nombres', 'Teléfono', 'Celular', 'Correo', 'Estado'],
                             lambda: buscar_estudiantes(texto))
    
    def _form_docente(self):
        """Formulario de docente como modal."""
        modal = ModernModal(self.root, "Nuevo Docente", "400x350")
        
        inner = tk.Frame(modal, bg=LinearDesign.COLORS['bg_surface'],
                        padx=LinearDesign.SPACE['xl'], pady=LinearDesign.SPACE['xl'])
        inner.pack(fill='both', expand=True)
        
        fields = [('nombres', 'Nombres *'), ('telefono', 'Teléfono'),
                 ('celular', 'Celular *'), ('correo', 'Correo *'),
                 ('especializacion', 'Especialización')]
        
        entries = {}
        
        for key, label in fields:
            tk.Label(inner, text=label, font=LinearDesign.FONTS['body'],
                    fg=LinearDesign.COLORS['text_secondary'],
                    bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w', pady=(LinearDesign.SPACE['md'], 4))
            
            entry = ModernEntry(inner, width=32)
            entry.pack(fill='x')
            entries[key] = entry
        
        btn_frame = tk.Frame(inner, bg=LinearDesign.COLORS['bg_surface'])
        btn_frame.pack(pady=LinearDesign.SPACE['xl'], fill='x')
        
        ModernButton(btn_frame, "Guardar", lambda: self._save_docente(entries, modal),
                    variant='primary').pack(side='left', padx=4)
        ModernButton(btn_frame, "Cancelar", modal.destroy,
                    variant='ghost').pack(side='left', padx=4)
    
    def _save_docente(self, entries, modal):
        """Guarda docente."""
        datos = {k: v.get() for k, v in entries.items()}
        
        if not datos['nombres'] or not datos['celular'] or not datos['correo']:
            messagebox.showerror("Error", "Campos requeridos")
            return
        
        result = registrar_docente(
            nombres_completos=datos['nombres'],
            telefono=datos['telefono'] or None,
            celular=datos['celular'],
            correo_electronico=datos['correo'],
            especializacion=datos['especializacion'] or None
        )
        
        if result['exito']:
            messagebox.showinfo("Éxito", result['mensaje'])
            modal.destroy()
            self.show_docentes()
        else:
            messagebox.showerror("Error", result['error'])
    
    def _form_curso(self):
        """Formulario de curso como modal."""
        modal = ModernModal(self.root, "Nuevo Curso", "450x480")
        
        inner = tk.Frame(modal, bg=LinearDesign.COLORS['bg_surface'],
                        padx=LinearDesign.SPACE['xl'], pady=LinearDesign.SPACE['xl'])
        inner.pack(fill='both', expand=True)
        
        fields = [('codigo', 'Código *'), ('nombre', 'Nombre *'),
                 ('inicio', 'Fecha Inicio *'), ('fin', 'Fecha Fin *'),
                 ('hora_inicio', 'Hora Inicio'), ('hora_fin', 'Hora Fin'),
                 ('dias', 'Días'), ('inversion', 'Inversión')]
        
        entries = {}
        
        for key, label in fields:
            tk.Label(inner, text=label, font=LinearDesign.FONTS['body'],
                    fg=LinearDesign.COLORS['text_secondary'],
                    bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w', pady=(LinearDesign.SPACE['sm'], 2))
            
            entry = ModernEntry(inner, width=35)
            entry.pack(fill='x')
            entries[key] = entry
        
        # Default values
        entries['hora_inicio'].set('19:00')
        entries['hora_fin'].set('21:00')
        entries['dias'].set('Lunes,Miércoles,Viernes')
        entries['inversion'].set('150.0')
        
        btn_frame = tk.Frame(inner, bg=LinearDesign.COLORS['bg_surface'])
        btn_frame.pack(pady=LinearDesign.SPACE['lg'], fill='x')
        
        ModernButton(btn_frame, "Guardar", lambda: self._save_curso(entries, modal),
                    variant='primary').pack(side='left', padx=4)
        ModernButton(btn_frame, "Cancelar", modal.destroy,
                    variant='ghost').pack(side='left', padx=4)
    
    def _save_curso(self, entries, modal):
        """Guarda curso."""
        datos = {k: v.get() for k, v in entries.items()}
        
        if not datos['codigo'] or not datos['nombre']:
            messagebox.showerror("Error", "Código y nombre requeridos")
            return
        
        try:
            inversion = float(datos['inversion'])
        except:
            inversion = 150.0
        
        result = registrar_curso(
            codigo=datos['codigo'], nombre=datos['nombre'],
            modalidad='Online', fecha_inicio=datos['inicio'],
            fecha_fin=datos['fin'], horario_inicio=datos['hora_inicio'],
            horario_fin=datos['hora_fin'], dias_semana=datos['dias'],
            inversion=inversion
        )
        
        if result['exito']:
            messagebox.showinfo("Éxito", result['mensaje'])
            modal.destroy()
            self.show_cursos()
        else:
            messagebox.showerror("Error", result['error'])
    
    def _form_inscripcion(self):
        """Formulario de inscripción como modal."""
        modal = ModernModal(self.root, "Nueva Inscripción", "400x300")
        
        inner = tk.Frame(modal, bg=LinearDesign.COLORS['bg_surface'],
                        padx=LinearDesign.SPACE['xl'], pady=LinearDesign.SPACE['xl'])
        inner.pack(fill='both', expand=True)
        
        # Estudiante
        tk.Label(inner, text="Estudiante:", font=LinearDesign.FONTS['body'],
                fg=LinearDesign.COLORS['text_secondary'],
                bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w', pady=(0, 4))
        
        est_combo = ttk.Combobox(inner, font=LinearDesign.FONTS['body'], width=40,
                                values=[f"{e['nombres_completos']} ({e['identificacion']})" 
                                       for e in listar_estudiantes()])
        est_combo.pack(fill='x', pady=(0, LinearDesign.SPACE['md']))
        
        # Curso
        tk.Label(inner, text="Curso:", font=LinearDesign.FONTS['body'],
                fg=LinearDesign.COLORS['text_secondary'],
                bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w', pady=(0, 4))
        
        cur_combo = ttk.Combobox(inner, font=LinearDesign.FONTS['body'], width=40,
                                values=[f"{c['nombre']} ({c['codigo']})" 
                                       for c in listar_cursos(estado='activo')])
        cur_combo.pack(fill='x', pady=(0, LinearDesign.SPACE['md']))
        
        # Checkboxes
        pdf_var = tk.BooleanVar(value=True)
        tk.Checkbutton(inner, text="Tiene copia de cédula PDF", variable=pdf_var,
                      font=LinearDesign.FONTS['body'],
                      bg=LinearDesign.COLORS['bg_surface'],
                      fg=LinearDesign.COLORS['text_primary']).pack(anchor='w')
        
        pago_var = tk.BooleanVar(value=True)
        tk.Checkbutton(inner, text="Tiene comprobante de pago", variable=pago_var,
                      font=LinearDesign.FONTS['body'],
                      bg=LinearDesign.COLORS['bg_surface'],
                      fg=LinearDesign.COLORS['text_primary']).pack(anchor='w')
        
        # Buttons
        btn_frame = tk.Frame(inner, bg=LinearDesign.COLORS['bg_surface'])
        btn_frame.pack(pady=LinearDesign.SPACE['lg'], fill='x')
        
        def save():
            if est_combo.current() < 0 or cur_combo.current() < 0:
                messagebox.showerror("Error", "Seleccione estudiante y curso")
                return
            
            estudiantes = listar_estudiantes()
            cursos = listar_cursos(estado='activo')
            
            result = inscribir_estudiante(
                id_estudiante=estudiantes[est_combo.current()]['id_estudiante'],
                id_curso=cursos[cur_combo.current()]['id_curso'],
                tiene_pdf_cedula=pdf_var.get(),
                tiene_pago=pago_var.get()
            )
            
            if result['exito']:
                messagebox.showinfo("Éxito", result['mensaje'])
                modal.destroy()
                self.show_inscripciones()
            else:
                messagebox.showerror("Error", result['error'])
        
        ModernButton(btn_frame, "Inscribir", save,
                    variant='primary').pack(side='left', padx=4)
        ModernButton(btn_frame, "Cancelar", modal.destroy,
                    variant='ghost').pack(side='left', padx=4)
    
    def _form_certificado(self):
        """Formulario de certificado como modal."""
        modal = ModernModal(self.root, "Generar Certificado", "380x220")
        
        inner = tk.Frame(modal, bg=LinearDesign.COLORS['bg_surface'],
                        padx=LinearDesign.SPACE['xl'], pady=LinearDesign.SPACE['xl'])
        inner.pack(fill='both', expand=True)
        
        # Inscripción
        tk.Label(inner, text="Inscripción:", font=LinearDesign.FONTS['body'],
                fg=LinearDesign.COLORS['text_secondary'],
                bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w', pady=(0, 4))
        
        ins_combo = ttk.Combobox(inner, font=LinearDesign.FONTS['body'], width=35,
                                values=[f"{i['nombre_estudiante']} - {i['nombre_curso']}" 
                                       for i in listar_inscripciones(estado='inscrito')])
        ins_combo.pack(fill='x', pady=(0, LinearDesign.SPACE['md']))
        
        # Calificación
        tk.Label(inner, text="Calificación:", font=LinearDesign.FONTS['body'],
                fg=LinearDesign.COLORS['text_secondary'],
                bg=LinearDesign.COLORS['bg_surface']).pack(anchor='w', pady=(0, 4))
        
        calif_spin = tk.Spinbox(inner, from_=0, to=100, font=LinearDesign.FONTS['body'], width=33)
        calif_spin.set(80)
        calif_spin.pack(fill='x')
        
        # Buttons
        btn_frame = tk.Frame(inner, bg=LinearDesign.COLORS['bg_surface'])
        btn_frame.pack(pady=LinearDesign.SPACE['lg'], fill='x')
        
        def save():
            if ins_combo.current() < 0:
                messagebox.showerror("Error", "Seleccione inscripción")
                return
            
            try:
                calif = float(calif_spin.get())
            except:
                messagebox.showerror("Error", "Calificación inválida")
                return
            
            inscripciones = listar_inscripciones(estado='inscrito')
            result = generar_certificado(
                id_inscripcion=inscripciones[ins_combo.current()]['id_inscripcion'],
                calificacion=calif
            )
            
            if result['exito']:
                messagebox.showinfo("Éxito", f"{result['mensaje']}\n\nCert: {result['numero_certificado']}")
                modal.destroy()
                self.show_certificados()
            else:
                messagebox.showerror("Error", result['error'])
        
        ModernButton(btn_frame, "Generar", save,
                    variant='primary').pack(side='left', padx=4)
        ModernButton(btn_frame, "Cancelar", modal.destroy,
                    variant='ghost').pack(side='left', padx=4)
    
    def run(self):
        """Inicia la aplicación."""
        self.root.mainloop()


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

def main():
    """Inicia con pantalla de login."""
    def on_login_success(usuario):
        app = ABACOMApp(usuario)
        app.run()
    
    login = LoginScreen(on_login_success)
    login.run()


if __name__ == "__main__":
    main()