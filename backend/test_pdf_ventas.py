from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
import os

# Carga plantilla HTML
env = Environment(loader=FileSystemLoader('generador_pdf/templates'))
template = env.get_template('acta_despacho_ventas.html')

# Simulación de datos
data = {
    'fecha': '07/08/2025',
    'factura': 'FAC-67890',
    'cliente': 'ACME S.A.',
    'productos': [
        {
            'cantidad': 10,
            'descripcion': 'Producto A largo nombre con especificaciones',
            'lote': 'L12345',
            'vencimiento': '12/09/2025',
            'rs': 'RS001',
            'checks': [True, False, True, True, False, True, True],  # exactos 7 elementos
            'condicion': 'Refrigerado'
        },
        
    ]
}
# Renderizar HTML con los datos
html_out = template.render(**data)

# Ruta de salida
fecha_carpeta = datetime.strptime(data['fecha'], "%d/%m/%Y").strftime("%d-%m-%Y")
output_folder = os.path.join("ActaDespachoVentas", fecha_carpeta)
os.makedirs(output_folder, exist_ok=True)
pdf_path = os.path.join(output_folder, f"{data['factura']}.pdf")

# Ruta absoluta a la carpeta de imágenes y CSS
STATIC_ABS = os.path.abspath("generador_pdf/static")

# Generar el PDF
HTML(string=html_out, base_url=STATIC_ABS).write_pdf(pdf_path)

print(f"✅ PDF generado correctamente: {pdf_path}")
