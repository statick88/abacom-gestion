# Sistema de Gestión Educativa ABACOM

> **Instituto de Tecnología y Ciencias**
> 
> Proyecto final del Curso de Python Fundamentos - Módulo 10
> 
> Desarrollado por: Diego Medardo Saavedra García

---

## 📋 Descripción

Sistema de gestión educativa completo para administrar estudiantes, cursos, inscripciones y certificaciones del Instituto ABACOM.

## 🚀 Características

- ✅ **Gestión de Estudiantes**: Registro con validación de cédula Ecuador (10 dígitos)
- ✅ **Gestión de Docentes**: CRUD completo de facilitadores
- ✅ **Gestión de Cursos**: Creación con período académico, modalidad, horarios
- ✅ **Inscripciones**: Registro con requisitos (PDF cédula + pago)
- ✅ **Certificaciones**: Generación con aval del Ministerio del Trabajo
- ✅ **Reportes**: Estadísticas y exportación CSV

## 🛠️ Tecnologías

| Componente | Tecnología |
|------------|------------|
| Base de Datos | SQLite3 |
| Lenguaje | Python 3.14+ |
| GUI | PyQt5 |
| Web | Flask |
| PDF | ReportLab |
| Tests | pytest |

## 📁 Estructura

```
abacom-gestion/
├── config.py              # Configuración global
├── main.py                # Punto de entrada
├── requirements.txt        # Dependencias
├── database/
│   ├── schema.sql        # Esquema de DB
│   └── abacom.db         # Base de datos
├── models/
│   ├── database.py       # Conexión y consultas
│   └── entities.py       # 4 clases POO
├── services/
│   ├── servicios.py      # Lógica de negocio
│   └── pdf_generator.py # Generación PDF
├── console/
│   └── app.py           # Interfaz CLI
├── gui/
│   └── app.py           # Interfaz PyQt5
├── web/
│   └── app.py           # Interfaz Flask
├── specs/
│   └── test_reglas_negocio.py  # 20 pruebas
├── test_e2e.py          # 8 pruebas E2E
└── pdfs/                 # Certificados generados
```

## 📊 Tests

| Tipo | Cantidad | Estado |
|------|----------|--------|
| Spec Tests (pytest) | 20 | ✅ Todos pasan |
| End-to-End | 8 | ✅ Todos pasan |
| **Total** | **28** | ✅ |

## ⚡ Uso Rápido

```bash
# Clonar el repositorio
git clone git@github.com:statick88/abacom-gestion.git
cd abacom-gestion/

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar interfaz de consola
python3 main.py
# Seleccionar opción 1

# O ejecutar directamente
python3 console/app.py

# Ejecutar GUI (requiere PyQt5)
python3 main.py
# Seleccionar opción 2
pip install PyQt5

# Ejecutar tests
python3 -m pytest specs/ -v

# Ejecutar todos los tests E2E
python3 test_e2e.py
```

## 🎓 Relación con el Curso

Este proyecto es el **Proyecto Final** del curso de Python Fundamentos de ABACOM.

Ubicación en el curso: `~/dev/apps/Abacom/course_of_python/content/modulo-10/proyecto-sistema-gestion-abacom.qmd`

El documento del curso referencia este repositorio como: `github.com/statick88/abacom-gestion`

## 📝 Licencia

MIT License - Instituto ABACOM

---

**Autor**: Diego Medardo Saavedra García  
**Instituto**: ABACOM - Instituto de Tecnología y Ciencias  
**Versión**: 1.0.0