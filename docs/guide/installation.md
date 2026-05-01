# Guía de Instalación - ABACOM Gestión

## Opciones de Instalación

### Opción 1: Descargar Ejecutable (Recomendado)

| Plataforma | Archivo | Link |
|------------|---------|------|
| Windows | `ABACOM_Gestion.exe` | GitHub Releases |
| macOS | `ABACOM_Gestion_1.0.0.dmg` | GitHub Releases |
| Linux | `ABACOM_Gestion_1.0.0_amd64.deb` | GitHub Releases |

### Opción 2: Desde Código Fuente

#### Requisitos Previos
```bash
# Python 3.8+
python3 --version

# Git
git --version
```

#### Pasos

```bash
# 1. Clonar repositorio
git clone https://github.com/<tu-usuario>/abacom-gestion.git
cd abacom-gestion

# 2. Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 5. Ejecutar aplicación
python3 gui/app.py
```

## Primer Inicio

### Configurar Admin
El sistema requiere un usuario administrador. Establecer credenciales via entorno:

```bash
# Linux/macOS
export ABACOM_ADMIN_USER="admin"
export ABACOM_ADMIN_PASSWORD="tu_password_seguro"
export ABACOM_ADMIN_EMAIL="admin@abacom.edu.ec"

# Windows (PowerShell)
$env:ABACOM_ADMIN_USER="admin"
$env:ABACOM_ADMIN_PASSWORD="tu_password_seguro"
$env:ABACOM_ADMIN_EMAIL="admin@abacom.edu.ec"
```

### Credenciales por Defecto (desarrollo)
```
Usuario: statick
Password: [configurado en primer setup]
```

## Verificar Instalación

```bash
# Ejecutar tests
pytest -v

# Verificar GUI
python3 -c "from gui.app import main; print('OK')"
```

## Actualización

```bash
# Pull latest
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt

# Migrar DB si es necesario
python3 scripts/migrate.py
```

## Desinstalación

### Windows
- Panel de Control → Programs → ABACOM Gestión → Uninstall

### macOS
```bash
rm -rf /Applications/ABACOM_Gestion.app
rm -rf ~/Library/Application\ Support/ABACOM
```

### Linux
```bash
sudo dpkg -r abacom-gestion
```

---

**Soporte técnico**: soporte@abacom.edu.ec