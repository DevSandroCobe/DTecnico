# Conexion/conexion_sql.py
import pyodbc
from Config.conexion_config import CONFIG_SQL

class ConexionSQL:
    def __init__(self):
        self.conexion = None
        self.cursor = None
        self.db_estado = False

    def __enter__(self):
        self.conectar()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cerrar_conexion()

    def conectar(self):
        try:
            conn_str = (
                f"DRIVER={{SQL Server}};"
                f"SERVER={CONFIG_SQL['server']};"
                f"DATABASE={CONFIG_SQL['database']};"
                f"UID={CONFIG_SQL['user']};"
                f"PWD={CONFIG_SQL['password']};"
                f"TrustServerCertificate=yes;"
            )
            self.conexion = pyodbc.connect(conn_str)
            self.cursor = self.conexion.cursor()
            self.db_estado = True
        except Exception as e:
            print("❌ Error al conectar a SQL Server:", str(e))
            self.db_estado = False

    def valida_conexion(self):
        return self.db_estado

    def ejecutar(self, query: str):
        if not self.valida_conexion():
            print("⚠️ Conexión no válida")
            return None
        try:
            self.cursor.execute(query)
            self.conexion.commit()
            return self.cursor
        except Exception as e:
            print(f"❌ Error ejecutando query SQL: {e}")
            return None

    def obtener_todos(self):
        try:
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ Error al obtener resultados: {e}")
            return []

    def cerrar_conexion(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
