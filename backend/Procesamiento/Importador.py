import html
import datetime

class Importador:
    def __init__(self):
        # Lista de bloques de queries SQL. Inicia con 'USE SAP' para definir el contexto.
        self.query_sql = ["USE SAP"]
        self.estado = "procesando"
        self.contador = 0      # Contador de registros en el bloque actual
        self.i = 0             # Índice del bloque actual
        self.limite = 400      # Máximo de inserts por bloque

    def _sanitize(self, val):
        # Escapa caracteres especiales para prevenir errores en el SQL (aunque no previene inyección)
        return html.escape(str(val), quote=True)

    def _insert(self, tabla_sql, valores):
        # Si se excede el límite de registros por bloque, inicia un nuevo bloque
        if self.contador > self.limite:
            self.contador = 0
            self.i += 1
            self.query_sql.append("")

        # Construye el VALUES('val1','val2',...) con sanitización básica
        values_str = ", ".join(f"'{self._sanitize(val)}'" for val in valores)
        insert_stmt = f"\nINSERT INTO {tabla_sql} VALUES({values_str})"

        # Agrega el INSERT al bloque actual
        self.query_sql[self.i] += insert_stmt
        self.contador += 1

    def query_transaccion(self, reg_hana, tabla_sql):
        """
        Recibe un registro de SAP HANA (lista de valores) y el nombre de la tabla SQL.
        Usa un mapeo para saber qué columnas tomar de reg_hana para cada tabla.
        """
        tabla_map = {
            "OITM": [0, 1, 2, 3, 4, 5, 6],
            "OWHS": [0, 1, 2],
            "OWTR": list(range(11)),
            "WTR1": list(range(6)),
            "OITL": list(range(7)),
            "ODLN": list(range(13)),
            "OINV": [0, 1, 2],
            "OBTW": list(range(5)),
            "OBTN": [0, 1, 2, 3, 4, 5],
            "ITL1": list(range(5)),
            "IBT1": list(range(7)),
            "DLN1": list(range(7)),
            "INV1": list(range(9)),
        }

        if tabla_sql in tabla_map:
            indices = tabla_map[tabla_sql]
            valores = []

            for idx in indices:
                val = reg_hana[idx]

                # Si la tabla es OBTN y la columna es fecha (índice 5), convertirla al formato esperado
                if tabla_sql == "OBTN" and idx == 5:
                    if isinstance(val, str):
                        try:
                            fecha = datetime.datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
                            val = fecha.strftime("%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            val = ""  # Si no se puede convertir, lo dejamos vacío

                valores.append(val)

            # Genera y guarda el INSERT
            self._insert(tabla_sql, valores)