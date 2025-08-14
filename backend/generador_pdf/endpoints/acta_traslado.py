import logging
import traceback
from pydantic import BaseModel
from datetime import date
from fastapi import APIRouter, HTTPException
from Conexion.conexion_sql import ConexionSQL
from generador_pdf.pdf_generator import generar_pdf_acta_traslado

# Agrega esto junto con tus otros imports
from typing import Optional

# --------------------------------------------------------
# Configuración del Logger
# --------------------------------------------------------
LOG_FILE = "pdf_traslado.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --------------------------------------------------------
# Router
# --------------------------------------------------------
router = APIRouter()

class PDFTrasladoRequest(BaseModel):
    fecha: date

@router.post("/generar_pdf_traslado/")
def generar_pdf_traslado(data: PDFTrasladoRequest):
    fecha = data.fecha.strftime("%Y-%m-%d")
    logger.info(f"➡ Fecha recibida: {fecha}")

    try:
        # 1️⃣ Obtener lista de DocEntries
        with ConexionSQL() as conn:
            cursor = conn.cursor
            logger.info(f"📦 Ejecutando SP: LISTADO_DOC_DESPACHO_TRASLADOS '{fecha}'")
            cursor.execute("{CALL LISTADO_DOC_DESPACHO_TRASLADOS (?)}", fecha)
            rows = cursor.fetchall()
            docentries = [row[0] for row in rows]
            logger.info(f"➡ DocEntries encontrados: {docentries}")

        rutas_generadas = []

        # 2️⃣ Procesar cada DocEntry
        for docentry in docentries:
            with ConexionSQL() as conn:
                cursor = conn.cursor
                logger.info(f"🔍 Obteniendo datos para DocEntry {docentry}")
                cursor.execute("EXEC INFO_DOC_DESPACHO_TRASLADOS ?", docentry)
                columnas = [col[0] for col in cursor.description]
                registros = [dict(zip(columnas, row)) for row in cursor.fetchall()]

            if not registros:
                logger.warning(f"⚠️ DocEntry {docentry} no tiene registros. Saltando.")
                continue

            encabezado = registros[0]
            productos = registros[1:]

            logger.info(f"📄 Generando PDF para DocEntry {docentry} | Guia: {encabezado.get('NroGuia')}")

            # Formatear productos para el PDF
            productos_formateados = []
            for item in productos:
                try:
                    fecha_vcto = f"{item['Dia']:02d}/{item['Mes']:02d}/{item['Anio'] + 2000}"
                except KeyError:
                    fecha_vcto = "N/A"

                productos_formateados.append({
                    "cantidad": item.get("CantidadLote", 0),
                    "descripcion": item.get("NombreComercial", ""),
                    "lote": item.get("NroLote", ""),
                    "serie": item.get("MnfSerial", ""),
                    "vencimiento": fecha_vcto,
                    "rs": item.get("MnfSerial", ""),
                    "condicion": item.get("CondicionAlm", ""),
                    "checks": [True, True,True, True,True, True,True],  # Ajusta esto según tus datos reales
                })

            fecha_str = data.fecha.strftime("%d-%m-%Y")


            data_pdf = {
                "fecha": fecha_str,
                "guia": encabezado["NroGuia"],       # Cambiado de GuiaRemision a NroGuia
                "AlmOrigen": encabezado["AlmOrigen"],   # Cambiado de AlmacenOrigen a AlmOrigen
                "AlmDestino": encabezado["AlmDestino"], # Cambiado de AlmacenDestino a AlmDestino
                "productos": productos,
                        }

            try:
                ruta = generar_pdf_acta_traslado(data_pdf)
                logger.info(f"✅ PDF generado: {ruta}")
                rutas_generadas.append(ruta)
            except Exception as pdf_error:
                logger.error(f"❌ Error generando PDF para DocEntry {docentry}: {pdf_error}")
                logger.debug(traceback.format_exc())

        logger.info(f"🏁 Proceso finalizado. Total PDFs: {len(rutas_generadas)}")
        return {"estado": "ok", "archivos_generados": rutas_generadas}

    except Exception as e:
        logger.critical(f"🔥 Error en generar_pdf_traslado: {e}")
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generando PDF traslado: {str(e)}")




# Agrega este modelo Pydantic
class VerificarMigracionRequest(BaseModel):
    fecha: date
    grupo: str

# Agrega este endpoint (junto con tus otros routers)
@router.get("/verificar_migracion/")
def verificar_migracion(fecha: str, grupo: str):
    """
    Verifica si los datos para una fecha y grupo específico ya fueron migrados
    """
    logger.info(f"🔍 Verificando migración para fecha: {fecha}, grupo: {grupo}")

    try:
        # 1️⃣ Validar parámetros
        if grupo.lower() != "traslados":
            return {"migrado": False, "mensaje": "Grupo no válido"}

        # 2️⃣ Consultar a la base de datos
        with ConexionSQL() as conn:
            cursor = conn.cursor  # <-- CORRECTO, no llamar como función
            # Consulta para verificar si existen registros para esa fecha
            query = """
            SELECT COUNT(*) 
            FROM OWTR 
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