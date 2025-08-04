from Conexion.conexion_sql import ConexionSQL
from Conexion.conexion_hana import ConexionHANA

def test_sql():
    sql = ConexionSQL("SELECT GETDATE()")
    sql.valida_conexion()
    print("SQL Server OK ✅" if sql.db_estado else "SQL Server FAIL ❌")
    sql.cerrar_conexion()

def test_hana():
    hana = ConexionHANA("SELECT * FROM DUMMY")
    hana.valida_conexion()
    print("SAP HANA OK ✅" if hana.db_estado else "SAP HANA FAIL ❌")
    hana.cerrar_conexion()

if __name__ == "__main__":
    test_sql()
    test_hana()
