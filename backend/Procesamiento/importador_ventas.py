from datetime import datetime

class ImportadorVenta:
    def __init__(self):
        self.inserts = {
            'ODLN': [],
            'DLN1': [],
            'OITL': [],
            'ITL1': [],
            'OBTN': [],
            'OBTW': [],
            'OITM': []
        }

    def _str(self, val):
        return f"'{str(val)}'"

    def agregar_odln(self, fila):
        # Ajustar índices según columnas de ODLN
        stmt = f"INSERT INTO ODLN VALUES({','.join([self._str(x) for x in fila[0:12]])})"
        self.inserts['ODLN'].append(stmt)

    def agregar_dln1(self, fila):
        # Ajustar índices según columnas de DLN1
        stmt = f"INSERT INTO DLN1 VALUES({','.join([self._str(x) for x in fila[12:20]])})"
        self.inserts['DLN1'].append(stmt)

    def agregar_oitl(self, fila):
        stmt = f"INSERT INTO OITL VALUES({','.join([self._str(x) for x in fila[20:27]])})"
        self.inserts['OITL'].append(stmt)

    def agregar_itl1(self, fila):
        stmt = f"INSERT INTO ITL1 VALUES({','.join([self._str(x) for x in fila[27:32]])})"
        self.inserts['ITL1'].append(stmt)

    def agregar_obtn(self, fila):
        stmt = f"INSERT INTO OBTN VALUES({','.join([self._str(x) for x in fila[32:38]])})"
        self.inserts['OBTN'].append(stmt)

    def agregar_obtw(self, fila):
        stmt = f"INSERT INTO OBTW VALUES({','.join([self._str(x) for x in fila[38:43]])})"
        self.inserts['OBTW'].append(stmt)

    def agregar_oitm(self, fila):
        stmt = f"INSERT INTO OITM VALUES({','.join([self._str(x) for x in fila[43:50]])})"
        self.inserts['OITM'].append(stmt)

    def procesar_fila(self, fila):
        self.agregar_odln(fila)
        self.agregar_dln1(fila)
        self.agregar_oitl(fila)
        self.agregar_itl1(fila)
        self.agregar_obtn(fila)
        self.agregar_obtw(fila)
        self.agregar_oitm(fila)

    def obtener_bloques(self, tabla):
        return self.inserts.get(tabla, [])
