import logging
import traceback
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from Conexion.conexion_sql import ConexionSQL
from generador_pdf.pdf_generator import generar_pdf_acta_ventas

router = APIRouter()

# Configuración de logging
LOG_FILE = "pdf_ventas.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PDFVentasRequest(BaseModel):
    fecha: date

@router.post("/generar_pdf_ventas/")
def generar_pdf_ventas(data: PDFVentasRequest):
    fecha = data.fecha.strftime("%Y-%m-%d")
    logger.info(f"➡ Fecha recibida: {fecha}")
    try:
        with ConexionSQL() as conn:
            cursor = conn.cursor
            logger.info(f"📦 Ejecutando SP: LISTADO_DOC_ENTREGA_VENTA '{fecha}'")
            cursor.execute("EXEC LISTADO_DOC_ENTREGA_VENTA ?", fecha)
            docentries = [row[0] for row in cursor.fetchall()]
            logger.info(f"➡ DocEntries encontrados: {docentries}")

        rutas_generadas = []

        for docentry in docentries:
            with ConexionSQL() as conn:
                cursor = conn.cursor
                logger.info(f"🔍 Obteniendo datos para DocEntry {docentry}")
                cursor.execute("EXEC INFO_DOC_ENTREGA_VENTA ?", docentry)
                columnas = [col[0] for col in cursor.description]
                registros = [dict(zip(columnas, row)) for row in cursor.fetchall()]

            if not registros:
                logger.warning(f"⚠️ DocEntry {docentry} no tiene registros. Saltando.")
                continue

            encabezado = registros[0]
            productos = registros[1:]

            # Formatear productos si es necesario (aquí se deja igual)
            data_pdf = {
                "fecha": encabezado["Fecha"],
                "factura": encabezado["Factura"],
                "cliente": encabezado["Cliente"],
                "productos": productos,
            }

            try:
                ruta = generar_pdf_acta_ventas(data_pdf)
                logger.info(f"✅ PDF generado: {ruta}")
                rutas_generadas.append(ruta)
            except Exception as pdf_error:
                logger.error(f"❌ Error generando PDF para DocEntry {docentry}: {pdf_error}")
                logger.debug(traceback.format_exc())

        logger.info(f"🏁 Proceso finalizado. Total PDFs: {len(rutas_generadas)}")
        return {"estado": "ok", "archivos_generados": rutas_generadas}

    except Exception as e:
        logger.critical(f"🔥 Error en generar_pdf_ventas: {e}")
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generando PDF ventas: {str(e)}")

# Endpoint para verificar migración de ventas
@router.get("/verificar_migracion/")
def verificar_migracion(fecha: str, grupo: str):
    logger.info(f"🔍 Verificando migración para fecha: {fecha}, grupo: {grupo}")
    try:
        if grupo.lower() != "ventas":
            return {"migrado": False, "mensaje": "Grupo no válido"}
        with ConexionSQL() as conn:
            cursor = conn.cursor
            query = """
            SELECT COUNT(*) 
            FROM ODLN 
            WHERE CONVERT(date, Docdate) = ?
            """
            cursor.execute(query, fecha)
            count = cursor.fetchone()[0]
            migrado = count > 0
            mensaje = f"Datos {'ya migrados' if migrado else 'no migrados'} para {fecha}"
            logger.info(f"✔ Resultado verificación: {mensaje}")
            return {
                "migrado": migrado,
                "mensaje": mensaje,
                "detalle": {
                    "fecha_consultada": fecha,
                    "registros_encontrados": count
                }
            }
    except Exception as e:
        logger.error(f"❌ Error verificando migración: {str(e)}")
        logger.debug(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error al verificar migración: {str(e)}"
        )
