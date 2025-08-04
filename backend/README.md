# 📄 Generador de PDFs de Actas de Despacho (Python + WeasyPrint)

Este módulo forma parte de la migración del sistema legacy en PHP hacia una arquitectura moderna con Python y Vue.js. Utiliza **WeasyPrint** para generar documentos PDF de actas de despacho, replicando y mejorando la lógica previamente implementada con `dompdf`.

---

## 🧠 Objetivo

Automatizar la generación de PDFs a partir de datos extraídos de SAP (HANA o SQL Server), organizándolos en formato HTML estilizado, y renderizándolos a PDF con alta calidad y soporte completo de CSS.

---

## 📦 Tecnologías usadas

| Componente | Tecnología |
|-----------|------------|
pip install python-dotenv

| Backend PDF | [WeasyPrint](https://weasyprint.org/) |
| Template Engine | [Jinja2](https://jinja.palletsprojects.com/) |
| Extracción de datos | SAP HANA / SQL Server mediante `pyhdb` o `pyodbc` |
| Lenguaje | Python 3.x |

---

## ✅ ¿Por qué WeasyPrint?

> Elegido como reemplazo natural de `dompdf` por su compatibilidad con HTML+CSS y su soporte moderno.

- ✅ Renderiza HTML + CSS modernos (Flexbox, Grid, fuentes, etc.)
- ✅ Soporta encabezados, pies, imágenes y tablas con excelente resolución
- ✅ Permite separación lógica de presentación (HTML) y lógica de datos (Python)
- ✅ Genera documentos multi-página
- ✅ Fácil integración en servidores o procesos por lotes

---

## 🚀 Instalación

### 1. Instalar dependencias del sistema (Linux)

```bash
sudo apt install libpangocairo-1.0-0 libpangoft2-1.0-0 libcairo2 libgdk-pixbuf2.0-0
