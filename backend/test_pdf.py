from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
import os

# Configuración de entorno Jinja2
TEMPLATES_PATH = os.path.join("generador_pdf", "templates")
STATIC_PATH = os.path.join("generador_pdf", "static")

env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
template = env.get_template('acta_despacho_traslado.html')

# Datos simulados (coinciden con lo que espera la plantilla real)
data = {
    'fecha': '14-08-2025',  # igual que el formato del endpoint
    'guia': 'GUIA-12345',
    'AlmOrigen': 'ALMACÉN PRINCIPAL',
    'AlmDestino': 'SUCURSAL A',
    'productos': [
        {
            'CantidadLote': 10,
            'NombreComercial': 'Producto A',
            'Concentracion': '500mg',
            'FormaFarmaceutica': 'Tableta',
            'FormaPresentacion': 'Caja x 10',
            'NroLote': 'L12345',
            'Dia': 12,
            'Mes': 9,
            'Anio': 2025,
            'RegistroSanit': 'RS001',
            'CondicionAlm': 'Refrigerado'
        },
        {
            'CantidadLote': 5,
            'NombreComercial': 'Producto B',
            'Concentracion': '250mg',
            'FormaFarmaceutica': 'Cápsula',
            'FormaPresentacion': 'Blister x 20',
            'NroLote': 'B98765',
            'Dia': 1,
            'Mes': 10,
            'Anio': 2026,
            'RegistroSanit': 'RS002',
            'CondicionAlm': 'Temperatura ambiente'
        }
    ]
}

# Renderizar HTML con datos
html_out = template.render(**data)

# Crear carpeta de salida basada en la fecha
fecha_carpeta = datetime.strptime(data['fecha'], "%d-%m-%Y").strftime("%d-%m-%Y")
output_folder = os.path.join("ActaDespacho_trasl", fecha_carpeta)
os.makedirs(output_folder, exist_ok=True)

# Ruta completa para guardar el PDF
pdf_path = os.path.join(output_folder, f"{data['guia']}.pdf")

# Generar PDF desde HTML
HTML(string=html_out, base_url=os.path.abspath(STATIC_PATH)).write_pdf(pdf_path)

print(f"✅ PDF generado exitosamente en: {os.path.abspath(pdf_path)}")
