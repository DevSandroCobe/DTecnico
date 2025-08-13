import logging
import time
import traceback
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
import os

# Módulos locales
from Migrador.migrador import Migrador
from Migrador.migrador_traslado import Migrador_traslado, MigracionTrasladoRequest
from Migrador.migrador_ventas import MigradorVentas
from generador_pdf.endpoints import acta_ventas, acta_traslado  


# --------------------------------------------------------
# Configuración de Logging
# --------------------------------------------------------
LOG_FILE = "migracion.log"
logging.basicConfig(
    level=logging.INFO,  # Cambia a DEBUG si quieres más detalle
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  # También imprime en consola
    ]
)
logger = logging.getLogger(__name__)

# --------------------------------------------------------
# Inicialización de la app
# --------------------------------------------------------
app = FastAPI(title="API de Migración y Generación de PDFs")

# --------------------------------------------------------
# CORS
# --------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# --------------------------------------------------------
# Modelos de entrada
# --------------------------------------------------------
class MigracionRequest(BaseModel):
    fecha: date
    tabla: str = "*"

class MigracionTrasladoRequest(BaseModel):
    fecha: date

class MigracionVentasRequest(BaseModel):
    fecha: date

# --------------------------------------------------------
# Endpoints
# --------------------------------------------------------
@app.post("/")
def root():
    return {"mensaje": "✅ API Migrador funcionando correctamente"}

@app.post("/api/importar/")
async def importar_data(request: MigracionRequest = Body(...)):
    fecha_str = request.fecha.isoformat()
    logger.info(f"📅 Solicitud de migración para la fecha: {fecha_str}, tabla: {request.tabla}")

    try:
        migrador = Migrador(fecha_str=fecha_str)

        tablas = (
            ["OITM", "OWHS", "OWTR", "WTR1", "OITL", "ODLN",
             "OINV", "OBTW", "OBTN", "ITL1", "DLN1", "INV1", "IBT1"]
            if request.tabla == "*" else [request.tabla]
        )

        resultados = {}
        for tabla in tablas:
            logger.info(f"▶ Iniciando migración de tabla {tabla}")
            start_time = time.perf_counter()
            try:
                resultado = migrador.migrar_tabla(tabla)
                duracion = round(time.perf_counter() - start_time, 2)
                logger.info(f"✅ Tabla {tabla} migrada en {duracion} segundos")
                resultados[tabla] = {"status": "ok", "mensaje": resultado, "tiempo": duracion}
            except Exception as e:
                duracion = round(time.perf_counter() - start_time, 2)
                error_trace = traceback.format_exc()
                logger.error(f"❌ Error en tabla {tabla} ({duracion}s): {e}\n{error_trace}")
                resultados[tabla] = {"status": "error", "mensaje": str(e), "tiempo": duracion}

        logger.info("🏁 Migración completada")
        return {"status": "success", "fecha": fecha_str, "resultados": resultados}

    except Exception as e:
        error_trace = traceback.format_exc()
        logger.critical(f"🔥 Error inesperado en importar_data: {e}\n{error_trace}")
        raise HTTPException(status_code=500, detail=f"❌ Error inesperado: {str(e)}")

@app.post("/api/importar_traslados/")
async def importar_traslados(request: MigracionTrasladoRequest = Body(...)):
    fecha_str = request.fecha.strftime('%Y-%m-%d')
    logger.info(f"📅 Solicitud de migración de traslados para la fecha: {fecha_str}")
    try:
        migrador = Migrador_traslado(request.fecha)
        resultados = migrador.migrar_todas()
        logger.info("🏁 Migración de traslados completada")
        return {"status": "success", "fecha": fecha_str, "resultados": resultados}
    except Exception as e:
        error_trace = traceback.format_exc()
        logger.critical(f"🔥 Error inesperado en importar_traslados: {e}\n{error_trace}")
        raise HTTPException(status_code=500, detail=f"❌ Error inesperado: {str(e)}")

@app.post("/api/importar_ventas/")
async def importar_ventas(request: MigracionVentasRequest = Body(...)):
    fecha_str = request.fecha.strftime('%Y-%m-%d')
    logger.info(f"📅 Solicitud de migración de ventas para la fecha: {fecha_str}")
    try:
        migrador = MigradorVentas(request.fecha)
        resultados = migrador.migrar_todas()
        logger.info("🏁 Migración de ventas completada")
        return {"status": "success", "fecha": fecha_str, "resultados": resultados}
    except Exception as e:
        error_trace = traceback.format_exc()
        logger.critical(f"🔥 Error inesperado en importar_ventas: {e}\n{error_trace}")
        raise HTTPException(status_code=500, detail=f"❌ Error inesperado: {str(e)}")

# --------------------------------------------------------
# Routers adicionales
# --------------------------------------------------------
app.include_router(acta_ventas.router, prefix="/api")
app.include_router(acta_traslado.router, prefix="/api")

