import pyodbc
from Config.conexion_config import CONFIG_HANA

class ConexionHANA:
    def __init__(self, query =None ):
        self.conexion = None
        self.cursor = None
        self.db_estado = False
        self.query = query

    def __enter__(self):
        self.conectar()
        if self.query:
            self.ejecutar(self.query)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cerrar_conexion()

    def conectar(self):
        try:
            conn_str = (
                f"DSN={CONFIG_HANA['dsn']};"
                f"UID={CONFIG_HANA['user']};"
                f"PWD={CONFIG_HANA['password']}"
            )
            self.conexion = pyodbc.connect(conn_str)
            self.cursor = self.conexion.cursor()
            self.db_estado = True
        except Exception as e:
            print("❌ Error al conectar a SAP HANA:", str(e))
            self.db_estado = False

    def ejecutar(self, query: str):
        if self.db_estado and self.cursor:
            try:
                self.cursor.execute(query)
                return self.cursor
            except Exception as e:
                print(f"❌ Error al ejecutar query HANA: {e}")
        return None

    def obtener_registro(self):
        if self.db_estado and self.cursor:
            return self.cursor.fetchone()
        return None

    def obtener_tabla(self):
        if self.db_estado and self.cursor:
            return self.cursor.fetchall()
        return []

    def cerrar_conexion(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
