from datetime import datetime
from Conexion.conexion_hana import ConexionHANA
from Conexion.conexion_sql import ConexionSQL
from Procesamiento.Importador import Importador
from Procesamiento.importador_ventas import ImportadorVentas
from Config.conexion_config import CONFIG_HANA
from pydantic import BaseModel


class MigracionVentasRequest(BaseModel):
    fecha: datetime


class MigradorVentas:
    def __init__(self, fecha: datetime):
        self.fecha = fecha if isinstance(fecha, datetime) else datetime.strptime(str(fecha), "%Y-%m-%d")
        self.importador = Importador()
        self.tablas_objetivo = ['ENTREGAS_VENTA', 'OINV', 'INV1', 'OWHS', 'IBT1']
        self.queries = self._construir_queries()

    def _esquema(self, tabla):
        return CONFIG_HANA["schema"]

    def _formato_fecha_hana(self, columna):
        return f"TO_VARCHAR({columna}, 'YYYY-MM-DD')"

    def _construir_queries(self):
        esq = self._esquema("")
        fecha_str = self.fecha.strftime('%Y-%m-%d')
        # Consulta principal de entregas de venta (ODLN como tabla principal)
        consulta_entrega = f'''
            SELECT
              ODLN."DocEntry", ODLN."ObjType", ODLN."DocNum", ODLN."CardCode", ODLN."CardName", ODLN."NumAtCard", ODLN."DocDate", ODLN."TaxDate", ODLN."U_SYP_MDTD", ODLN."U_SYP_MDSD", ODLN."U_SYP_MDCD", ODLN."U_COB_LUGAREN", ODLN."U_BPP_FECINITRA",
              DLN1."DocEntry", DLN1."ObjType", DLN1."WhsCode", DLN1."ItemCode", DLN1."LineNum", DLN1."Dscription", DLN1."UomCode",
              IBT1."ItemCode", IBT1."BatchNum", IBT1."WhsCode", IBT1."BaseEntry", IBT1."BaseType", IBT1."BaseLinNum", IBT1."Quantity",
              INV1."DocEntry", INV1."ObjType", INV1."WhsCode", INV1."ItemCode", INV1."LineNum", INV1."Dscription", INV1."UomCode", INV1."BaseType", INV1."BaseEntry",
              ITL1."LogEntry", ITL1."ItemCode", ITL1."Quantity", ITL1."SysNumber", ITL1."MdAbsEntry",
              OBTN."ItemCode", OBTN."DistNumber", OBTN."SysNumber", OBTN."AbsEntry", OBTN."MnfSerial", OBTN."ExpDate",
              OBTW."ItemCode", OBTW."MdAbsEntry", OBTW."WhsCode", OBTW."Location", OBTW."AbsEntry",
              OITM."ItemCode", OITM."ItemName", OITM."FrgnName", OITM."U_SYP_CONCENTRACION", OITM."U_SYP_FORPR", OITM."U_SYP_FFDET", OITM."U_SYP_FABRICANTE",
              OINV."DocEntry", OINV."NumAtCard", OINV."U_SYP_NGUIA",
              OITL."LogEntry", OITL."ItemCode", OITL."DocEntry", OITL."DocLine", OITL."DocType", OITL."StockEff", OITL."LocCode",
              OWHS."WhsCode", OWHS."WhsName", OWHS."TaxOffice"
            FROM {self._esquema("ODLN")}.ODLN ODLN
            INNER JOIN {self._esquema("DLN1")}.DLN1 ON DLN1."DocEntry" = ODLN."DocEntry"
            INNER JOIN {self._esquema("IBT1")}.IBT1 ON IBT1."BaseEntry" = DLN1."DocEntry" AND IBT1."BaseType" = DLN1."ObjType" AND IBT1."WhsCode" = DLN1."WhsCode" AND IBT1."ItemCode" = DLN1."ItemCode" AND IBT1."BaseLinNum" = DLN1."LineNum" AND IBT1."Quantity" < 0
            INNER JOIN {self._esquema("OBTN")}.OBTN ON OBTN."ItemCode" = DLN1."ItemCode" AND OBTN."DistNumber" = IBT1."BatchNum"
            INNER JOIN {self._esquema("OITL")}.OITL ON OITL."DocEntry" = DLN1."DocEntry" AND OITL."ItemCode" = IBT1."ItemCode" AND OITL."DocType" = DLN1."ObjType" AND OITL."DocLine" = DLN1."LineNum" AND OITL."StockEff" = 1
            INNER JOIN {self._esquema("ITL1")}.ITL1 ON ITL1."LogEntry" = OITL."LogEntry" AND ITL1."SysNumber" = OBTN."SysNumber"
            LEFT JOIN {self._esquema("OBTW")}.OBTW ON OBTW."ItemCode" = DLN1."ItemCode" AND OBTW."MdAbsEntry" = ITL1."MdAbsEntry" AND OBTW."WhsCode" = DLN1."WhsCode"
            INNER JOIN {self._esquema("OITM")}.OITM ON OITM."ItemCode" = DLN1."ItemCode"
            LEFT JOIN {self._esquema("OINV")}.OINV ON OINV."U_SYP_NGUIA" = ODLN."NumAtCard"
            LEFT JOIN {self._esquema("INV1")}.INV1 ON INV1."DocEntry" = OINV."DocEntry"
            LEFT JOIN {self._esquema("OWHS")}.OWHS ON OWHS."WhsCode" = DLN1."WhsCode"
            WHERE {self._formato_fecha_hana('ODLN."DocDate"')} = '{fecha_str}'
              AND ODLN."CANCELED" = 'N'
              AND ODLN."U_COB_LUGAREN" IN ('15','16')
        '''
        consulta_oinv = f'''
            SELECT T0."DocEntry", T0."NumAtCard", T0."U_SYP_NGUIA"
            FROM {self._esquema("OINV")}.OINV T0
            WHERE T0."CANCELED" = 'N'
              AND T0."DocDate" = '{fecha_str}'
        '''
        consulta_inv1 = f'''
            SELECT T0."DocEntry", T0."ObjType", T0."WhsCode", T0."ItemCode", T0."LineNum", T0."Dscription",
                   T0."UomCode", T0."BaseType", T0."BaseEntry"
            FROM {self._esquema("INV1")}.INV1 T0
            INNER JOIN {self._esquema("OINV")}.OINV T1 ON T0."DocEntry" = T1."DocEntry"
            WHERE T1."CANCELED" = 'N'
              AND T1."DocDate" = '{fecha_str}'
        '''
        consulta_owhs = f'''
            SELECT T0."WhsCode", T0."WhsName", T0."TaxOffice"
            FROM {self._esquema("OWHS")}.OWHS T0
        '''
        consulta_ibt1 = f'''
            SELECT T0."ItemCode", T0."BatchNum", T0."WhsCode", T0."BaseEntry", T0."BaseType", T0."BaseLinNum", T0."Quantity"
            FROM {self._esquema("IBT1")}.IBT1 T0
            WHERE T0."Quantity" < 0 AND {self._formato_fecha_hana('T0."DocDate"')} = '{fecha_str}'
        '''

        return {
            'ENTREGAS_VENTA': consulta_entrega,
            'OINV': consulta_oinv,
            'INV1': consulta_inv1,
            'OWHS': consulta_owhs,
            'IBT1': consulta_ibt1
        }

    def migracion_hana_sql(self, query: str, tabla_sql: str) -> int:
        print(f"\n🚀 Migrando {tabla_sql}...")
        try:
            with ConexionHANA(query) as hana:
                if not hana.db_estado:
                    print("❌ Conexión a SAP HANA fallida")
                    return 0
                registros = hana.obtener_tabla()
                total = len(registros)
                print(f"📥 Registros extraídos de HANA: {total}")
                if not registros:
                    print(f"⚠️ No hay registros en {tabla_sql}")
                    return 0
                if tabla_sql == 'ENTREGAS_VENTA':
                    importador = ImportadorVentas()
                    for i, fila in enumerate(registros, 1):
                        importador.procesar_fila(fila)
                        if i % 100 == 0:
                            print(f"📤 Procesados {i} registros...")
                    tablas = ['ODLN', 'DLN1', 'IBT1', 'INV1', 'ITL1', 'OBTN', 'OBTW', 'OITM', 'OINV', 'OITL', 'OWHS']
                    with ConexionSQL() as sql:
                        if not sql.db_estado:
                            print("❌ Conexión a SQL Server fallida")
                            return 0
                        cursor = sql.cursor
                        for t in tablas:
                            try:
                                cursor.execute(f"TRUNCATE TABLE dbo.{t}")
                                print(f"🧹 Tabla dbo.{t} truncada exitosamente.")
                            except Exception as e:
                                print(f"⚠️ Error al truncar dbo.{t}: {e}")
                            bloques = importador.obtener_bloques(t)
                            for j, bloque in enumerate(bloques, 1):
                                if not bloque.strip():
                                    continue
                                try:
                                    print(f"🛰️ Ejecutando bloque {j} de {t}...")
                                    cursor.execute(bloque)
                                except Exception as e:
                                    print(f"❌ Error en bloque {j} ({t}): {e}")
                                    print(f"🔎 Bloque problemático:\n{bloque}")
                        sql.conexion.commit()
                        print(f"✅ Insertados en SQL Server: {total} registros de ENTREGAS_VENTA")
                        return total
                else:
                    self.importador = Importador()
                    for i, fila in enumerate(registros, 1):
                        self.importador.query_transaccion(fila, tabla_sql)
                        if i % 100 == 0:
                            print(f"📤 Procesados {i} registros...")
                    with ConexionSQL() as sql:
                        if not sql.db_estado:
                            print("❌ Conexión a SQL Server fallida")
                            return 0
                        cursor = sql.cursor
                        try:
                            cursor.execute(f"TRUNCATE TABLE dbo.{tabla_sql}")
                            print(f"🧹 Tabla dbo.{tabla_sql} truncada exitosamente.")
                        except Exception as e:
                            print(f"⚠️ Error al truncar dbo.{tabla_sql}: {e}")
                        bloques = self.importador.query_sql
                        for j, bloque in enumerate(bloques, 1):
                            if not bloque.strip():
                                continue
                            try:
                                print(f"🛰️ Ejecutando bloque {j} de {tabla_sql}...")
                                cursor.execute(bloque)
                            except Exception as e:
                                print(f"❌ Error en bloque {j} ({tabla_sql}): {e}")
                                print(f"🔎 Bloque problemático:\n{bloque}")
                        sql.conexion.commit()
                        print(f"✅ Insertados en SQL Server: {total} registros de {tabla_sql}")
                        return total
        except Exception as e:
            print(f"❌ Error migrando {tabla_sql}: {e}")
            return 0

    def migrar_todas(self) -> list:
        resultados = []
        for tabla in self.tablas_objetivo:
            cantidad = self.migracion_hana_sql(self.queries[tabla], tabla)
            resultados.append({
                "tabla": tabla,
                "fecha": self.fecha.strftime("%Y-%m-%d"),
                "registros": cantidad,
                "exito": cantidad > 0
            })
        return resultados
