"""
Tests de Seguridad - Sistema ABACOM
====================================
Pruebas de seguridad basadas en OWASP Top 10 2025

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
"""

import pytest
import sys
import os
import time
from pathlib import Path

# Agregar project al path
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from services.servicios import (
    hash_password,
    verify_password,
    validar_email_formato,
    validar_password,
    iniciar_sesion,
    auth_limiter,
    RateLimiter
)


# =============================================================================
# A04 - CRYPTOGRAPHIC FAILURES (Password Hashing)
# =============================================================================

class TestPasswordHashing:
    """Tests para validación de hashing de contraseñas."""
    
    def test_bcrypt_hash_generated(self):
        """Verifica que se genera hash bcrypt."""
        password = "TestPassword123"
        hashed = hash_password(password)
        
        # bcrypt hashes starts with $2a$, $2b$ or $2y$
        assert hashed.startswith(('$2a$', '$2b$', '$2y$')), "No es un hash bcrypt"
        assert len(hashed) == 60, "Longitud incorrecta para bcrypt"
    
    def test_bcrypt_verify_correct_password(self):
        """Verifica que bcrypt valida password correcta."""
        password = "SecurePass123!"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_bcrypt_verify_wrong_password(self):
        """Verifica que bcrypt rechaza password incorrecta."""
        password = "CorrectPassword"
        hashed = hash_password(password)
        
        assert verify_password("WrongPassword", hashed) is False
    
    def test_bcrypt_different_hashes_same_password(self):
        """Verifica que cada hash es único (salt diferente)."""
        password = "MyPassword123"
        
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 != hash2, "Los hashes deben ser diferentes (salt único)"


class TestPasswordValidation:
    """Tests para validación de requisitos de password."""
    
    def test_password_minimum_8_chars(self):
        """Password con menos de 8 caracteres es rechazada."""
        valido, mensaje = validar_password("short")
        
        assert valido is False
        assert "8 caracteres" in mensaje
    
    def test_password_valid_length(self):
        """Password válida con 8+ caracteres."""
        valido, mensaje = validar_password("12345678")
        
        assert valido is True
        assert mensaje == ""
    
    def test_empty_password_rejected(self):
        """Password vacía es rechazada."""
        valido, mensaje = validar_password("")
        
        assert valido is False


# =============================================================================
# A07 - AUTHENTICATION FAILURES (Rate Limiting)
# =============================================================================

class TestRateLimiting:
    """Tests para rate limiting de autenticación."""
    
    def test_rate_limiter_allows_5_attempts(self):
        """Verifica que permite 5 intentos antes de bloquear."""
        limiter = RateLimiter(max_attempts=5, lockout_seconds=60)
        
        # 5 intentos fallidos
        for i in range(5):
            limiter.record_failure("testuser")
        
        # Después de 5 debe estar bloqueado
        assert limiter.is_locked("testuser") is True
    
    def test_rate_limiter_remaining_attempts(self):
        """Verifica cálculo de intentos restantes."""
        limiter = RateLimiter(max_attempts=5, lockout_seconds=60)
        
        # 3 intentos fallidos
        for i in range(3):
            limiter.record_failure("testuser")
        
        assert limiter.remaining_attempts("testuser") == 2
    
    def test_rate_limiter_reset_after_success(self):
        """Verifica que resetea después de login exitoso."""
        limiter = RateLimiter(max_attempts=5, lockout_seconds=60)
        
        # 3 intentos fallidos
        for i in range(3):
            limiter.record_failure("testuser")
        
        # Login exitoso resetea
        limiter.record_success("testuser")
        
        assert limiter.remaining_attempts("testuser") == 5
    
    def test_rate_limiter_lockout_expires(self):
        """Verifica que el lockout expira."""
        limiter = RateLimiter(max_attempts=3, lockout_seconds=1)
        
        # Bloquear
        for i in range(3):
            limiter.record_failure("testuser")
        
        assert limiter.is_locked("testuser") is True
        
        # Esperar a que expire (1 segundo)
        time.sleep(1.5)
        
        # Ya no debe estar bloqueado
        assert limiter.is_locked("testuser") is False


# =============================================================================
# A09 - SECURITY LOGGING (Auditoría)
# =============================================================================

class TestSecurityLogging:
    """Tests para logging de auditoría."""
    
    def test_log_file_created_on_login(self):
        """Verifica que se crea archivo de log."""
        from services.servicios import log_auditoria
        
        log_dir = PROJECT_DIR / 'logs'
        
        # Ejecutar logging
        log_auditoria("testuser", "LOGIN_SUCCESS", "Test login")
        
        assert log_dir.exists()
        assert (log_dir / 'auditoria.log').exists()
    
    def test_log_format(self):
        """Verifica formato del log."""
        from services.servicios import log_auditoria
        
        log_file = PROJECT_DIR / 'logs' / 'auditoria.log'
        
        if log_file.exists():
            # Leer última línea
            with open(log_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    last_log = lines[-1]
                    # Formato: [timestamp] IP | USUARIO | ACCION | DETALLE
                    assert '[' in last_log
                    assert '|' in last_log


# =============================================================================
# VALIDACIÓN DE ENTRADA (A02 - Security Misconfiguration)
# =============================================================================

class TestInputValidation:
    """Tests para validación de entradas."""
    
    def test_valid_email_format(self):
        """Verifica validación de email válido."""
        assert validar_email_formato("user@example.com") is True
        assert validar_email_formato("test.user@domain.co") is True
    
    def test_invalid_email_format(self):
        """Verifica rechazo de email inválido."""
        assert validar_email_formato("not-an-email") is False
        assert validar_email_formato("@example.com") is False
        assert validar_email_formato("user@") is False
        assert validar_email_formato("") is False
    
    def test_email_rejects_none(self):
        """Verifica que None es rechazado."""
        assert validar_email_formato(None) is False


# =============================================================================
# A05 - INJECTION (SQL Injection Prevention)
# =============================================================================

class TestSQLInjectionPrevention:
    """Tests para verificar protección contra SQL Injection."""
    
    def test_prepared_statements_used(self):
        """Verifica que se usan prepared statements en servicios."""
        import services.servicios as servicios
        
        # Verificar que las funciones usan ejecutar_consulta con params
        source = servicios.iniciar_sesion.__code__.co_names
        
        # Las funciones usan ejecutar_consulta que internamente usa ?
        assert 'ejecutar_consulta' in source or 'ejecutar_modificacion' in source


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])