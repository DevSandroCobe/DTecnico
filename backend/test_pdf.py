from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
import os

# Configuración de entorno Jinja2
env = Environment(loader=FileSystemLoader('generador_pdf/templates'))
template = env.get_template('acta_despacho_traslado.html')

# Datos simulados
data = {
    'fecha': '07/11/2025',
    'guia': 'GUIA-12345',
    'almacen_origen': 'ALMACÉN PRINCIPAL',
    'almacen_destino': 'SUCURSAL A',
    'productos': [
        {
            'cantidad': 10,
            'descripcion': 'Producto A largo nombre con especificaciones',
            'lote': 'L12345',
            'vencimiento': '12/09/2025',
            'rs': 'RS001',
            'checks': [True, True, True, True],
            'condicion': 'Refrigerado'
        },
        # Agrega más productos si deseas
    ]
}

# Renderizar HTML con datos
html_out = template.render(**data)

# Crear carpeta de salida basada en la fecha
fecha_carpeta = datetime.strptime(data['fecha'], "%d/%m/%Y").strftime("%d-%m-%Y")
output_folder = os.path.join("ActaDespacho_trasl", fecha_carpeta)
os.makedirs(output_folder, exist_ok=True)

# Ruta completa para guardar el PDF
pdf_path = os.path.join(output_folder, f"{data['guia']}.pdf")

# Ruta base absoluta para que WeasyPrint encuentre las imágenes (logo, firma, etc.)
STATIC_ABS_PATH = os.path.abspath("generador_pdf/static")

# Generar PDF desde HTML
HTML(string=html_out, base_url=STATIC_ABS_PATH).write_pdf(pdf_path)

print(f"✅ PDF generado exitosamente en: {pdf_path}")
