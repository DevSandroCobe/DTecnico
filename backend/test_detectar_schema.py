from Utils.detectar_schema import detectar_schema_tabla

tablas = ['OITM', 'OBTW', 'OBTN', 'IBT1', 'OWHS', 'OINV',
            'INV1', 'OITL', 'ITL1', 'ODLN', 'DLN1', 'OWTR', 'WTR1']  # Agrega las tuyas

for tabla in tablas:
    try:
        esquema = detectar_schema_tabla(tabla)
        print(f"✅ {tabla} está en el esquema: {esquema}")
    except Exception as e:
        print(f"❌ Error con {tabla}: {e}")

