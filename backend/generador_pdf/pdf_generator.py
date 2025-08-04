import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from Conexion.conexion_sql import ConexionBdAccesosSQL

class GeneradorPdfActa:
    def __init__(self, fecha, output_dir="output_pdfs"):
        self.fecha = fecha
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.env = Environment(loader=FileSystemLoader("generador_pdf"))

    def obtener_docentrys(self, procedimiento):
        conexion = ConexionBdAccesosSQL(f"EXEC {procedimiento} '{self.fecha}'")
        conexion.validar_conexion()
        resultados = conexion.obtener_todos()
        conexion.cerrar_conexion()
        return [fila[0] for fila in resultados]

    def obtener_datos_encabezado(self, docentry):
        conn = ConexionBdAccesosSQL(f"EXEC INFO_DOC_ENTREGA_VENTA {docentry}")
        conn.validar_conexion()
        encabezado = conn.obtener_uno_dict()
        conn.cerrar_conexion()
        return encabezado

    def obtener_datos_contenido(self, docentry):
        conn = ConexionBdAccesosSQL(f"EXEC INFO_DOC_ENTREGA_VENTA {docentry}")
        conn.validar_conexion()
        contenido = conn.obtener_todos_dict()
        conn.cerrar_conexion()
        return contenido

    def generar_pdf(self, docentry):
        encabezado = self.obtener_datos_encabezado(docentry)
        contenido = self.obtener_datos_contenido(docentry)

        template = self.env.get_template("plantilla_acta.html")
        html_content = template.render(encabezado=encabezado, contenido=contenido)

        output_path = os.path.join(self.output_dir, f"Acta_{docentry}.pdf")
        HTML(string=html_content).write_pdf(output_path)
        print(f"PDF generado: {output_path}")

    def generar_todos_los_pdfs(self):
        docentries = self.obtener_docentrys("LISTADO_DOC_ENTREGA_VENTA")
        for docentry in docentries:
            self.generar_pdf(docentry)
