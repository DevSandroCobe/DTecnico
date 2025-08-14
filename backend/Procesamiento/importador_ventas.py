from datetime import datetime

class ImportadorVentas:
    def __init__(self):
        self.inserts = {
            'ODLN': [],
            'DLN1': [],
            'OITL': [],
            'ITL1': [],
            'OBTN': [],
            'OBTW': [],
            'OITM': [],
            'OINV': [],
            'INV1': [],
            'OWHS': []
        }

    def _str(self, val):
        return f"'{str(val)}'"

    def agregar_odln(self, fila):
        # ODLN: DocEntry, ObjType, DocNum, CardCode, CardName, NumAtCard, DocDate, TaxDate, U_SYP_MDTD, U_SYP_MDSD, U_SYP_MDCD, U_COB_LUGAREN, U_BPP_FECINITRA
        stmt = f"INSERT INTO ODLN VALUES({','.join([self._str(x) for x in fila[43:56]])})"
        self.inserts['ODLN'].append(stmt)

    def agregar_dln1(self, fila):
        # DLN1: DocEntry, ObjType, WhsCode, ItemCode, LineNum, Dscription, UomCode
        stmt = f"INSERT INTO DLN1 VALUES({','.join([self._str(x) for x in fila[0:7]])})"
        self.inserts['DLN1'].append(stmt)

    def agregar_ibt1(self, fila):
        # IBT1: ItemCode, BatchNum, WhsCode, BaseEntry, BaseType, BaseLinNum, Quantity
        stmt = f"INSERT INTO IBT1 VALUES({','.join([self._str(x) for x in fila[7:14]])})"
        self.inserts['IBT1'].append(stmt)

    def agregar_inv1(self, fila):
        # INV1: DocEntry, ObjType, WhsCode, ItemCode, LineNum, Dscription, UomCode, BaseType, BaseEntry
        stmt = f"INSERT INTO INV1 VALUES({','.join([self._str(x) for x in fila[14:23]])})"
        self.inserts['INV1'].append(stmt)

    def agregar_itl1(self, fila):
        # ITL1: LogEntry, ItemCode, Quantity, SysNumber, MdAbsEntry
        stmt = f"INSERT INTO ITL1 VALUES({','.join([self._str(x) for x in fila[23:28]])})"
        self.inserts['ITL1'].append(stmt)

    def agregar_obtn(self, fila):
        # OBTN: ItemCode, DistNumber, SysNumber, AbsEntry, MnfSerial, ExpDate
        stmt = f"INSERT INTO OBTN VALUES({','.join([self._str(x) for x in fila[28:34]])})"
        self.inserts['OBTN'].append(stmt)

    def agregar_obtw(self, fila):
        # OBTW: ItemCode, MdAbsEntry, WhsCode, Location, AbsEntry
        stmt = f"INSERT INTO OBTW VALUES({','.join([self._str(x) for x in fila[34:39]])})"
        self.inserts['OBTW'].append(stmt)

    def agregar_oitm(self, fila):
        # OITM: ItemCode, ItemName, FrgnName, U_SYP_CONCENTRACION, U_SYP_FORPR, U_SYP_FFDET, U_SYP_FABRICANTE
        stmt = f"INSERT INTO OITM VALUES({','.join([self._str(x) for x in fila[39:46]])})"
        self.inserts['OITM'].append(stmt)

    def agregar_oinv(self, fila):
        # OINV: DocEntry, NumAtCard, U_SYP_NGUIA
        stmt = f"INSERT INTO OINV VALUES({','.join([self._str(x) for x in fila[56:59]])})"
        self.inserts['OINV'].append(stmt)

    def agregar_oitl(self, fila):
        # OITL: LogEntry, ItemCode, DocEntry, DocLine, DocType, StockEff, LocCode
        stmt = f"INSERT INTO OITL VALUES({','.join([self._str(x) for x in fila[59:66]])})"
        self.inserts['OITL'].append(stmt)

    def agregar_owhs(self, fila):
        # OWHS: WhsCode, WhsName, TaxOffice
        stmt = f"INSERT INTO OWHS VALUES({','.join([self._str(x) for x in fila[66:69]])})"
        self.inserts['OWHS'].append(stmt)

    def procesar_fila(self, fila):
        self.agregar_dln1(fila)
        self.agregar_ibt1(fila)
        self.agregar_inv1(fila)
        self.agregar_itl1(fila)
        self.agregar_obtn(fila)
        self.agregar_obtw(fila)
        self.agregar_oitm(fila)
        self.agregar_odln(fila)
        self.agregar_oinv(fila)
        self.agregar_oitl(fila)
        self.agregar_owhs(fila)

    def obtener_bloques(self, tabla):
        return self.inserts.get(tabla, [])
