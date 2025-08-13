import logging
import traceback
from Conexion.conexion_sql import ConexionSQL

logger = logging.getLogger(__name__)

# --------------------------------------------------------
# ENTREGA
# --------------------------------------------------------
def obtener_docentries_entrega(fecha: str):
    try:
        with ConexionSQL() as conn:
            if not conn.valida_conexion():
                logger.error("❌ Conexión SQL no válida en obtener_docentries_entrega()")
                return []
            logger.info(f"📦 Ejecutando: EXEC LISTADO_DOC_ENTREGA_VENTA '{fecha}'")
            conn.cursor.execute("EXEC LISTADO_DOC_ENTREGA_VENTA ?", fecha)
            resultados = [row[0] for row in conn.cursor.fetchall()]
            logger.info(f"✅ {len(resultados)} DocEntries encontrados para entrega")
            return resultados
    except Exception as e:
        logger.error(f"❌ Error en obtener_docentries_entrega({fecha}): {e}")
        logger.debug(traceback.format_exc())
        return []

def obtener_info_entrega(docentry: int):
    try:
        with ConexionSQL() as conn:
            if not conn.valida_conexion():
                logger.error("❌ Conexión SQL no válida en obtener_info_entrega()")
                return []
            logger.info(f"📦 Ejecutando: EXEC INFO_DOC_ENTREGA_VENTA {docentry}")
            conn.cursor.execute("EXEC INFO_DOC_ENTREGA_VENTA ?", docentry)
            columnas = [col[0] for col in conn.cursor.description]
            registros = [dict(zip(columnas, row)) for row in conn.cursor.fetchall()]
            logger.info(f"✅ {len(registros)} registros obtenidos para entrega {docentry}")
            return registros
    except Exception as e:
        logger.error(f"❌ Error en obtener_info_entrega({docentry}): {e}")
        logger.debug(traceback.format_exc())
        return []

# --------------------------------------------------------
# TRASLADO
# --------------------------------------------------------
def obtener_docentries_traslado(fecha: str):
    try:
        with ConexionSQL() as conn:
            if not conn.valida_conexion():
                logger.error("❌ Conexión SQL no válida en obtener_docentries_traslado()")
                return []
            logger.info(f"📦 Ejecutando: EXEC LISTADO_DOC_TRASLADO '{fecha}'")
            conn.cursor.execute("EXEC LISTADO_DOC_TRASLADO ?", fecha)
            resultados = [row[0] for row in conn.cursor.fetchall()]
            logger.info(f"✅ {len(resultados)} DocEntries encontrados para traslado")
            return resultados
    except Exception as e:
        logger.error(f"❌ Error en obtener_docentries_traslado({fecha}): {e}")
        logger.debug(traceback.format_exc())
        return []

def obtener_info_traslado(docentry: int):
    try:
        with ConexionSQL() as conn:
            if not conn.valida_conexion():
                logger.error("❌ Conexión SQL no válida en obtener_info_traslado()")
                return []
            logger.info(f"📦 Ejecutando: EXEC INFO_DOC_TRASLADO {docentry}")
            conn.cursor.execute("EXEC INFO_DOC_TRASLADO ?", docentry)
            columnas = [col[0] for col in conn.cursor.description]
            registros = [dict(zip(columnas, row)) for row in conn.cursor.fetchall()]
            logger.info(f"✅ {len(registros)} registros obtenidos para traslado {docentry}")
            return registros
    except Exception as e:
        logger.error(f"❌ Error en obtener_info_traslado({docentry}): {e}")
        logger.debug(traceback.format_exc())
        return []
