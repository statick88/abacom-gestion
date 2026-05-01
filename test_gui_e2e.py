"""
Tests E2E para GUI de escritorio (tkinter)
==========================================
Tests directamente con imports de Python.

Autor: Diego Medardo Saavedra García
"""

import sys
import os
from pathlib import Path

# Agregar proyecto al path
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

# Cambiar al directorio del proyecto
os.chdir(PROJECT_DIR)

import pytest


class TestGUIImports:
    """Tests de importación de la GUI."""
    
    def test_gui_module_imports(self):
        """Verifica que gui.app se puede importar."""
        from gui import app
        assert hasattr(app, 'LoginScreen')
        assert hasattr(app, 'ABACOMApp')
    
    def test_login_screen_class_exists(self):
        """Verifica que LoginScreen existe."""
        from gui.app import LoginScreen
        assert LoginScreen is not None
    
    def test_abacom_app_class_exists(self):
        """Verifica que ABACOMApp existe."""
        from gui.app import ABACOMApp
        assert ABACOMApp is not None
    
    def test_design_class_exists(self):
        """Verifica que LinearDesign existe."""
        from gui.app import LinearDesign
        assert LinearDesign is not None
    
    def test_modal_class_exists(self):
        """Verifica que ModernModal existe."""
        from gui.app import ModernModal
        assert ModernModal is not None


class TestAuthServices:
    """Tests de servicios de autenticación."""
    
    def test_iniciar_sesion_import(self):
        """Verifica que iniciar_sesion se puede importar."""
        from services.servicios import iniciar_sesion
        assert callable(iniciar_sesion)
    
    def test_registrar_usuario_import(self):
        """Verifica que registrar_usuario se puede importar."""
        from services.servicios import registrar_usuario
        assert callable(registrar_usuario)
    
    def test_validar_email_import(self):
        """Verifica que validar_email_formato se puede importar."""
        from services.servicios import validar_email_formato
        assert callable(validar_email_formato)
    
    def test_login_with_correct_credentials(self):
        """Verifica login con credenciales correctas."""
        from services.servicios import iniciar_sesion
        
        result = iniciar_sesion("statick", "a1b2d3d4*")
        
        assert result['exito'] is True
        assert 'usuario' in result
        assert result['usuario']['nombres'] == 'Diego Medardo Saavedra García'
    
    def test_login_with_wrong_password(self):
        """Verifica que rechaza password incorrecta."""
        from services.servicios import iniciar_sesion
        
        result = iniciar_sesion("statick", "wrongpassword")
        
        assert result['exito'] is False
        assert 'Credenciales incorrectas' in result['error']


class TestSecurity:
    """Tests de seguridad."""
    
    def test_bcrypt_hash_generated(self):
        """Verifica que se genera hash bcrypt."""
        from services.servicios import hash_password
        
        hashed = hash_password("test123")
        
        assert hashed.startswith('$2b$')
        assert len(hashed) == 60
    
    def test_bcrypt_verify_correct(self):
        """Verifica bcrypt con password correcta."""
        from services.servicios import hash_password, verify_password
        
        hashed = hash_password("test123")
        
        assert verify_password("test123", hashed) is True
    
    def test_rate_limiter_class(self):
        """Verifica que RateLimiter existe."""
        from services.servicios import RateLimiter
        
        limiter = RateLimiter(max_attempts=5, lockout_seconds=60)
        
        assert limiter.max_attempts == 5
        assert limiter.lockout_seconds == 60
    
    def test_rate_limiter_blocks(self):
        """Verifica que rate limiter bloquea después de 5 intentos."""
        from services.servicios import RateLimiter, auth_limiter
        
        # Usar el limiter global que se usa en iniciar_sesion
        # Resetear primero
        if "testuser" in auth_limiter._attempts:
            del auth_limiter._attempts["testuser"]
        
        # 5 intentos fallidos
        for i in range(5):
            auth_limiter.record_failure("testuser")
        
        assert auth_limiter.is_locked("testuser") is True
    
    def test_audit_log_function_exists(self):
        """Verifica que log_auditoria existe."""
        from services.servicios import log_auditoria
        assert callable(log_auditoria)


class TestDatabase:
    """Tests de base de datos."""
    
    def test_database_connection(self):
        """Verifica que se puede conectar a la DB."""
        from models.database import get_db_connection
        
        with get_db_connection() as conn:
            assert conn is not None
    
    def test_usuarios_table_exists(self):
        """Verifica que la tabla usuarios existe."""
        from models.database import ejecutar_consulta
        
        result = ejecutar_consulta("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        
        assert len(result) > 0
    
    def test_admin_user_exists(self):
        """Verifica que el usuario admin existe en la DB."""
        from models.database import ejecutar_consulta
        
        result = ejecutar_consulta(
            "SELECT usuario, email, rol FROM usuarios WHERE rol = 'admin'"
        )
        
        assert len(result) > 0
        assert result[0]['usuario'] == 'statick'
        assert result[0]['email'] == 'dsaavedra88@gmail.com'


class TestSpecs:
    """Tests de especificaciones."""
    
    def test_spec_tests_pass(self):
        """Verifica que los spec tests pasan."""
        import subprocess
        
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', 'specs/test_reglas_negocio.py', '-v', '--tb=short'],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Specs failed: {result.stdout}"
    
    def test_security_tests_pass(self):
        """Verifica que los tests de seguridad pasan."""
        import subprocess
        
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', 'specs/test_seguridad.py', '-v', '--tb=short'],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Security tests failed: {result.stdout}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])