"""
================================================================================
INTEGRACIÓN WHATSAPP BUSINESS - SISTEMA ABACOM
================================================================================
Gestión de grupos para facilitadores usando WhatsApp Business API.

Autor: Diego Medardo Saavedra García
Instituto: ABACOM
================================================================================
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from typing import Optional, List, Dict
import json
import sys
from pathlib import Path

# Configuración (simulada - en producción usar variables de entorno)
WHATSAPP_TOKEN = "tu_token_aqui"
WHATSAPP_PHONE_ID = "tu_phone_id"
WHATSAPP_API_VERSION = "v18.0"
WHATSAPP_BASE_URL = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_ID}"

# =============================================================================
# CLASE: WHATSAPPMANAGER
# =============================================================================

class WhatsAppManager:
    """Gestor de integración con WhatsApp Business API."""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or WHATSAPP_TOKEN
        self.phone_id = WHATSAPP_PHONE_ID
        self.base_url = WHATSAPP_BASE_URL
        self.mock_mode = (self.token == "tu_token_aqui")
    
    def send_message(self, to: str, message: str) -> Dict:
        """
        Envía un mensaje de WhatsApp.
        
        Args:
            to: Número de teléfono destino (formato: 593999999999)
            message: Contenido del mensaje
        
        Returns:
            dict: Resultado del envío
        """
        if self.mock_mode:
            # Simulación en modo desarrollo
            print(f"[MOCK] Enviando mensaje a {to}: {message[:50]}...")
            return {
                "exito": True,
                "message_id": "mock-msg-12345",
                "mensaje": "Mensaje enviado (simulado)"
            }
        
        # Implementación real (requiere requests)
        # import requests
        # url = f"{self.base_url}/messages"
        # headers = {
        #     "Authorization": f"Bearer {self.token}",
        #     "Content-Type": "application/json"
        # }
        # data = {
        #     "messaging_product": "whatsapp",
        #     "to": to,
        #     "type": "text",
        #     "text": {"body": message}
        # }
        # response = requests.post(url, headers=headers, json=data)
        # if response.status_code == 200:
        #     return {"exito": True, "message_id": response.json().get("messages")[0]["id"]}
        # else:
        #     return {"exito": False, "error": response.text}
        
        return {"exito": False, "error": "Modo real no implementado"}
    
    def create_group(self, name: str, participants: List[str]) -> Dict:
        """
        Crea un grupo de WhatsApp.
        
        Args:
            name: Nombre del grupo
            participants: Lista de números de teléfono
        
        Returns:
            dict: Información del grupo creado
        """
        if self.mock_mode:
            # Simulación
            group_id = f"mock-group-{hash(name) % 10000}"
            print(f"[MOCK] Creando grupo '{name}' con {len(participants)} participantes")
            return {
                "exito": True,
                "group_id": group_id,
                "name": name,
                "participants": participants,
                "mensaje": "Grupo creado (simulado)"
            }
        
        # Implementación real
        return {"exito": False, "error": "Modo real no implementado"}
    
    def add_participant(self, group_id: str, phone: str) -> Dict:
        """Agrega un participante a un grupo."""
        if self.mock_mode:
            print(f"[MOCK] Agregando {phone} al grupo {group_id}")
            return {"exito": True, "mensaje": "Participante agregado (simulado)"}
        return {"exito": False, "error": "Modo real no implementado"}
    
    def send_notification_to_group(self, group_id: str, message: str) -> Dict:
        """Envía una notificación a todo el grupo."""
        if self.mock_mode:
            print(f"[MOCK] Notificación al grupo {group_id}: {message[:50]}...")
            return {"exito": True, "mensaje": "Notificación enviada (simulado)"}
        return {"exito": False, "error": "Modo real no implementado"}


# =============================================================================
# SERVICIO: NOTIFICACIONES A FACILITADORES
# =============================================================================

def notificar_facilitador(id_curso: int, mensaje: str) -> Dict:
    """
    Envía notificación al facilitador del curso vía WhatsApp.
    
    Args:
        id_curso: ID del curso
        mensaje: Mensaje a enviar
    
    Returns:
        dict: Resultado de la notificación
    """
    from models.database import ejecutar_consulta
    
    # Obtener facilitador del curso
    query = """
        SELECT d.celular, d.nombres_completos, c.nombre as curso_nombre
        FROM cursos c
        LEFT JOIN docentes d ON c.id_docente = d.id_docente
        WHERE c.id_curso = ?
    """
    resultado = ejecutar_consulta(query, (id_curso,))
    
    if not resultado:
        return {"exito": False, "error": "Curso no encontrado"}
    
    docente = resultado[0]
    
    if not docente['celular']:
        return {"exito": False, "error": "Docente no tiene celular registrado"}
    
    # Enviar mensaje
    manager = WhatsAppManager()
    return manager.send_message(
        to=docente['celular'],
        message=f"📚 ABACOM - {docente['curso_nombre']}\n\n{mensaje}"
    )


def crear_grupo_curso(id_curso: int) -> Dict:
    """
    Crea un grupo de WhatsApp para un curso con todos los estudiantes inscritos.
    
    Args:
        id_curso: ID del curso
        
    Returns:
        dict: Información del grupo creado
    """
    from models.database import ejecutar_consulta
    
    # Obtener datos del curso
    curso = ejecutar_consulta(
        "SELECT nombre FROM cursos WHERE id_curso = ?",
        (id_curso,)
    )
    if not curso:
        return {"exito": False, "error": "Curso no encontrado"}
    
    # Obtener números de estudiantes inscritos
    query = """
        SELECT e.celular
        FROM inscripciones i
        JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
        WHERE i.id_curso = ? AND i.estado = 'inscrito'
    """
    estudiantes = ejecutar_consulta(query, (id_curso,))
    
    if not estudiantes:
        return {"exito": False, "error": "No hay estudiantes inscritos"}
    
    participants = [e['celular'] for e in estudiantes if e['celular']]
    
    # Crear grupo
    manager = WhatsAppManager()
    return manager.create_group(
        name=f"ABACOM - {curso[0]['nombre']}",
        participants=participants
    )


# =============================================================================
# PRUEBAS DE INTEGRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=== Integración WhatsApp - ABACOM ===\n")
    
    # 1. Probar envío de mensaje
    print("1. Enviando mensaje de prueba...")
    manager = WhatsAppManager()
    result = manager.send_message(
        to="593999999999",
        message="📚 Prueba de notificación ABACOM"
    )
    print(f"   {result}")
    
    # 2. Probar creación de grupo
    print("\n2. Creando grupo de prueba...")
    result = manager.create_group(
        name="ABACOM - Python Fundamentos",
        participants=["593999999991", "593999999992", "593999999993"]
    )
    print(f"   {result}")
    
    # 3. Probar notificación a facilitador (simulada)
    print("\n3. Notificando facilitador...")
    result = notificar_facilitador(15, "Recordatorio: Clase hoy a las 19:00")
    print(f"   {result}")
    
    # 4. Probar creación de grupo para curso
    print("\n4. Creando grupo para curso...")
    result = crear_grupo_curso(15)
    print(f"   {result}")
    
    print("\n✅ Integración WhatsApp completada (modo simulado)")
