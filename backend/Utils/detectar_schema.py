# detectar_schema.py
from Conexion.conexion_hana import ConexionHANA

def detectar_schema_tabla(nombre_tabla: str) -> str:
    query = f"""
        SELECT SCHEMA_NAME
        FROM SYS.TABLES
        WHERE TABLE_NAME = '{nombre_tabla.upper()}'
    """
    with ConexionHANA() as db:
        if db.db_estado:
            db.ejecutar(query)
            resultado = db.obtener_registro()
            if resultado:
                return resultado[0]
            else:
                raise ValueError(f"❌ No se encontró el esquema para la tabla {nombre_tabla}.")
        else:
            raise ConnectionError("❌ Error al conectar a SAP HANA.")
