from datetime import datetime

class Importador:
    def __init__(self):
        self.query_sql = ["USE SAP"]
        self.estado = "procesando"
        self.contador = 0
        self.i = 0
        self.limite = 400

    def _agregar_insert(self, tabla, valores):
        if self.contador >= self.limite:
            print(f"🧱 Límite alcanzado ({self.limite}) en bloque {self.i} de {tabla}. Generando nuevo bloque...")
            self.contador = 0
            self.i += 1
            self.query_sql.append("")

        insert_stmt = f"\nINSERT INTO {tabla} VALUES(" + ",".join(valores) + ")"
        self.query_sql[self.i] += insert_stmt
        self.contador += 1

    def _str(self, val):
        return f"'{str(val)}'"

    def query_transaccion(self, reg_hana, tabla):
        print(f"📥 Recibido registro para tabla {tabla}: {reg_hana}")
        try:
            if tabla == "OITM":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2]),
                    self._str(reg_hana[3]),
                    self._str(reg_hana[4]),
                    self._str(reg_hana[5]),
                    self._str(reg_hana[6])
                ])
            elif tabla == "OWHS":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2])
                ])
            elif tabla == "OWTR":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2]),
                    self._str(reg_hana[3]),
                    self._str(reg_hana[4]),
                    self._str(reg_hana[5]),
                    self._str(reg_hana[6]),
                    self._str(reg_hana[7]),
                    self._str(reg_hana[8]),
                    self._str(reg_hana[9]),
                    self._str(reg_hana[10])
                ])
            elif tabla == "WTR1":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2]),
                    self._str(reg_hana[3]),
                    self._str(reg_hana[4]),
                    self._str(reg_hana[5])
                ])
            elif tabla == "OITL":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2]),
                    self._str(reg_hana[3]),
                    self._str(reg_hana[4]),
                    self._str(reg_hana[5]),
                    self._str(reg_hana[6])
                ])
            elif tabla == "ODLN":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2]),
                    self._str(reg_hana[3]),
                    self._str(reg_hana[4]),
                    self._str(reg_hana[5]),
                    self._str(reg_hana[6]),
                    self._str(reg_hana[7]),
                    self._str(reg_hana[8]),
                    self._str(reg_hana[9]),
                    self._str(reg_hana[10]),
                    self._str(reg_hana[11]),
                    self._str(reg_hana[12])
                ])
            elif tabla == "OINV":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2])
                ])
            elif tabla == "OBTW":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2]),
                    self._str(reg_hana[3]),
                    self._str(reg_hana[4])
                ])
            elif tabla == "OBTN":
                try:
                    fecha = datetime.strptime(reg_hana[5], "%Y-%m-%d %H:%M:%S")
                    fecha_formateada = fecha.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    fecha_formateada = ""

                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2]),
                    self._str(reg_hana[3]),
                    self._str(reg_hana[4]),
                    self._str(fecha_formateada)
                ])
            elif tabla == "ITL1":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2]),
                    self._str(reg_hana[3]),
                    self._str(reg_hana[4])
                ])
            elif tabla == "IBT1":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2]),
                    self._str(reg_hana[3]),
                    self._str(reg_hana[4]),
                    self._str(reg_hana[5]),
                    self._str(reg_hana[6])
                ])
            elif tabla == "DLN1":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2]),
                    self._str(reg_hana[3]),
                    self._str(reg_hana[4]),
                    self._str(reg_hana[5]),
                    self._str(reg_hana[6])
                ])
            elif tabla == "INV1":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2]),
                    self._str(reg_hana[3]),
                    self._str(reg_hana[4]),
                    self._str(reg_hana[5]),
                    self._str(reg_hana[6]),
                    self._str(reg_hana[7]),
                    self._str(reg_hana[8])
                ])
            elif tabla == "TRASLADOS":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2]),
                    self._str(reg_hana[3]),
                    self._str(reg_hana[4]),
                    self._str(reg_hana[5]),
                    self._str(reg_hana[6]),
                    self._str(reg_hana[7]),
                    self._str(reg_hana[8]),
                    self._str(reg_hana[9]),
                    self._str(reg_hana[10]),
                    self._str(reg_hana[11]),
                    self._str(reg_hana[12]),
                    self._str(reg_hana[13]),
                    self._str(reg_hana[14]),
                    self._str(reg_hana[15]),
                    self._str(reg_hana[16]),
                    self._str(reg_hana[17]),
                    self._str(reg_hana[18])
                ])
            elif tabla == "ENTREGAS_VENTA":
                self._agregar_insert(tabla, [
                    self._str(reg_hana[0]),
                    self._str(reg_hana[1]),
                    self._str(reg_hana[2]),
                    self._str(reg_hana[3]),
                    self._str(reg_hana[4]),
                    self._str(reg_hana[5]),
                    self._str(reg_hana[6]),
                    self._str(reg_hana[7]),
                    self._str(reg_hana[8]),
                    self._str(reg_hana[9]),
                    self._str(reg_hana[10]),
                    self._str(reg_hana[11]),
                    self._str(reg_hana[12]),
                    self._str(reg_hana[13]),
                    self._str(reg_hana[14]),
                    self._str(reg_hana[15]),
                    self._str(reg_hana[16]),
                    self._str(reg_hana[17]),
                    self._str(reg_hana[18])
                ])
        except IndexError as e:
            print(f"❌ ERROR en {tabla}: índice fuera de rango en reg_hana → {e}")
        except Exception as e:
            print(f"❌ ERROR inesperado en {tabla}: {e}")
