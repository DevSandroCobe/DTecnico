from Conexion.conexion_hana import ConexionHANA
from Config.conexion_config import CONFIG_HANA

tablas = ['OITM', 'OBTW', 'OBTN', 'IBT1', 'OWHS', 'OINV',
          'INV1', 'OITL', 'ITL1', 'ODLN', 'DLN1', 'OWTR', 'WTR1']

schema = CONFIG_HANA.get("schema", "SBODEMOCL")

for tabla in tablas:
    query = f'SELECT TOP 1 * FROM "{schema}"."{tabla}"'  # Consulta simple de validación
    try:
        with ConexionHANA(query) as hana:
            if hana.db_estado:
                fila = hana.obtener_registro()
                print(f"✅ {tabla} encontrada en el esquema {schema}")
            else:
                print(f"❌ Conexión fallida al verificar {tabla}")
    except Exception as e:
        print(f"❌ Error con {tabla}: {e}")
