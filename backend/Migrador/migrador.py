from datetime import datetime, timedelta
from Conexion.conexion_hana import ConexionHANA
from Conexion.conexion_sql import ConexionSQL
from Procesamiento.Importador import Importador
from Utils.detectar_schema import detectar_schema_tabla


class Migrador:
    def __init__(self, fecha_str):
        self.fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        self.fecha_inicio = self.fecha.replace(hour=0, minute=0, second=0)
        self.fecha_fin = self.fecha_inicio + timedelta(days=1) - timedelta(seconds=1)
        self.importador = Importador()
        self.tablas_objetivo = [
            'OITM', 'OBTW', 'OBTN',  'OWHS', 'OINV',
            'INV1', 'OITL', 'ITL1', 'ODLN', 'DLN1', 'OWTR', 'WTR1'
        ]
        self.esquemas = self._detectar_esquemas()
        self.queries = self._construir_queries()

    def _detectar_esquemas(self):
        return {tabla: detectar_schema_tabla(tabla) for tabla in self.tablas_objetivo}

    def _esquema(self, tabla):
        return self.esquemas.get(tabla, 'SBODEMOCL')

    def _formato_fecha_hana(self, columna):
        return f"TO_NVARCHAR({columna}, 'YYYY-MM-DD')"

    def _construir_queries(self):
        return {
            'reset': "TRUNCATE TABLE dbo.TEMP_ENTREGA",
            'OITM': f'SELECT "ItemCode", "ItemName" FROM {self._esquema("OITM")}.OITM',
            'OBTW': f'''
                SELECT "ItemCode", "WhsCode", "BcdCode", "Quantity", "OnHand", "IsCommited"
                FROM {self._esquema("OBTW")}.OBTW''',
            'OBTN': f'''
                SELECT "ItemCode", "DistNumber", "SysNumber", "AbsEntry", "MnfSerial",
                       {self._formato_fecha_hana('"ExpDate"')} AS "ExpDate"
                FROM {self._esquema("OBTN")}.OBTN
                WHERE "ExpDate" > '{self.fecha:%Y-%m-%d}' ''',
            'IBT1': f'''
                SELECT "BaseEntry", "ItemCode", "WhsCode", "Quantity", 
                       "SysNumber", "BaseType", "BaseLinNum"
                FROM {self._esquema("IBT1")}.IBT1''',
            'OWHS': f'''
                SELECT "WhsCode", "WhsName"
                FROM {self._esquema("OWHS")}.OWHS''',
            'OINV': f'''
                SELECT "DocEntry", "DocNum", {self._formato_fecha_hana('"DocDate"')} AS "DocDate",
                       "CardCode", "CardName", "DocTotal"
                FROM {self._esquema("OINV")}.OINV
                WHERE "DocDate" BETWEEN '{self.fecha_inicio:%Y-%m-%d}' AND '{self.fecha_fin:%Y-%m-%d}' ''',
            'INV1': f'''
                SELECT "DocEntry", "LineNum", "ItemCode", "Quantity", 
                       "WhsCode", "BaseType"
                FROM {self._esquema("INV1")}.INV1''',
            'OITL': f'''
                SELECT "LogEntry", "ItemCode", "DocEntry", "DocType", "StockQty"
                FROM {self._esquema("OITL")}.OITL''',
            'ITL1': f'''
                SELECT "LogEntry", "ItemCode", "Quantity", "SysNumber"
                FROM {self._esquema("ITL1")}.ITL1''',
            'ODLN': f'''
                SELECT "DocEntry", "DocNum", {self._formato_fecha_hana('"DocDate"')} AS "DocDate",
                       "CardCode", "CardName"
                FROM {self._esquema("ODLN")}.ODLN
                WHERE "DocDate" BETWEEN '{self.fecha_inicio:%Y-%m-%d}' AND '{self.fecha_fin:%Y-%m-%d}' ''',
            'DLN1': f'''
                SELECT "DocEntry", "LineNum", "ItemCode", "Quantity", "WhsCode"
                FROM {self._esquema("DLN1")}.DLN1''',
            'OWTR': f'''
                SELECT "DocEntry", "DocNum", {self._formato_fecha_hana('"DocDate"')} AS "DocDate",
                       "Filler", "ToWhsCode"
                FROM {self._esquema("OWTR")}.OWTR
                WHERE "DocDate" BETWEEN '{self.fecha_inicio:%Y-%m-%d}' AND '{self.fecha_fin:%Y-%m-%d}' ''',
            'WTR1': f'''
                SELECT "DocEntry", "LineNum", "ItemCode", "Quantity", "WhsCode"
                FROM {self._esquema("WTR1")}.WTR1'''
        }

    def migracion_hana_sql(self, query: str, tabla_sql: str) -> int:
        print(f"🚀 Migrando {tabla_sql}...")
        try:
            with ConexionHANA(query) as hana:
                if not hana.db_estado:
                    raise RuntimeError("Conexión a HANA fallida")

                registros = hana.obtener_tabla()
                if not registros:
                    print(f"⚠️ No hay registros en {tabla_sql}")
                    return 0

                for i, fila in enumerate(registros, 1):
                    self.importador.query_transaccion(fila, tabla_sql)
                    if i % 100 == 0:
                        print(f"📤 Procesados {i} registros...")

            with ConexionSQL() as sql:
                if not sql.db_estado:
                    raise RuntimeError("Conexión a SQL Server fallida")
                return len(registros)

        except Exception as e:
            print(f"❌ Error migrando {tabla_sql}: {e}")
            return 0

    def ejecutar_reset(self) -> bool:
        try:
            with ConexionSQL() as sql:
                if sql.valida_conexion():
                    sql.ejecutar(self.queries['reset'])
                    print("🔁 Reset exitoso")
                    return True
        except Exception as e:
            print(f"❌ Error en reset: {e}")
        return False

    def migrar_tabla(self, tabla: str) -> tuple:
        if tabla not in self.queries:
            return 0, f"⚠️ Tabla {tabla} no encontrada"
        cantidad = self.migracion_hana_sql(self.queries[tabla], tabla)
        return cantidad, f"✅ Migración de {tabla}: {cantidad} registros"

    def migrar_todas(self) -> dict:
        resultados = {}
        if not self.ejecutar_reset():
            return {"error": "Falló el reset de SQL"}

        for tabla in self.tablas_objetivo:
            cantidad, mensaje = self.migrar_tabla(tabla)
            resultados[tabla] = {
                "registros": cantidad,
                "mensaje": mensaje,
                "exito": cantidad > 0
            }
        return resultados
