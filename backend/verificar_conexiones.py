from Conexion.conexion_sql import ConexionSQL
from Conexion.conexion_hana import ConexionHANA
from Config.conexion_config import CONFIG_HANA

def test_sql():
    sql = ConexionSQL()
    sql.conectar()
    if sql.db_estado:
        print("SQL Server OK ✅")
    else:
        print("SQL Server FAIL ❌")
    sql.cerrar_conexion()

def test_hana():
    tablas = ['OITM', 'OBTW', 'OBTN', 'IBT1', 'OWHS', 'OINV',
              'INV1', 'OITL', 'ITL1', 'ODLN', 'DLN1', 'OWTR', 'WTR1']
    errores = 0
    for tabla in tablas:
        query = f'SELECT TOP 1 * FROM {CONFIG_HANA["schema"]}."{tabla}"'
        try:
            with ConexionHANA(query) as hana:
                if hana.db_estado:
                    resultado = hana.obtener_registro()
                    if resultado:
                        print(f"✅ {tabla}: conexión y datos OK")
                    else:
                        print(f"⚠️ {tabla}: conexión OK, sin datos")
                else:
                    print(f"❌ {tabla}: error de conexión")
                    errores += 1
        except Exception as e:
            print(f"❌ {tabla}: {e}")
            errores += 1
    if errores == 0:
        print("🟢 Todas las tablas verificadas correctamente.")
    else:
        print(f"🔴 {errores} tabla(s) con problemas.")

if __name__ == "__main__":
    test_sql()
    test_hana()
