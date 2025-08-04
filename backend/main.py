from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from Migrador.migrador import Migrador

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class MigracionRequest(BaseModel):
    fecha: date  # Ya será un objeto date
    tabla: str = "*"

@app.post("/")
def root():
    return {"mensaje": "✅ API Migrador funcionando correctamente"}

@app.post("/api/importar/")
async def importar_data(request: MigracionRequest = Body(...)):
    print(f"📅 Fecha recibida: {request.fecha.isoformat()}")
    try:
        # Convertimos el date a string si hace falta para Migrador
        fecha_str = request.fecha.isoformat()
        migrador = Migrador(fecha_str=fecha_str)

        tablas = (
            ["OITM", "OWHS", "OWTR", "WTR1", "OITL", "ODLN",
             "OINV", "OBTW", "OBTN", "ITL1",  "DLN1", "INV1"]
            if request.tabla == "*" else [request.tabla]
        )

        resultados = {}
        for tabla in tablas:
            try:
                resultado = migrador.migrar_tabla(tabla)
                resultados[tabla] = {"status": "ok", "mensaje": resultado}
            except Exception as e:
                resultados[tabla] = {"status": "error", "mensaje": str(e)}

        return {"status": "success", "fecha": fecha_str, "resultados": resultados}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error inesperado: {str(e)}")
# # Endpoint opcional por si quieres truncar desde otro lugar
# @app.post("/api/truncate/{table_name}")
# def truncate_table(table_name: str):
#     try:
#         conn = get_sql_connection()
#         cursor = conn.cursor()

#         cursor.execute(f"TRUNCATE TABLE {table_name}")
#         conn.commit()
#         cursor.close()
#         conn.close()

#         return {"status": "ok", "message": f"Tabla {table_name} truncada correctamente."}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# # Si usas generación de PDFs (puedes comentar si no lo usas aún)
# @app.post("/api/generar_pdf/")
# def generar_pdf(data: dict):
#     fecha = data.get("fecha")
#     tipo = data.get("tipo")  # "traslado" o "venta"

#     if tipo == "traslado":
#         path = generar_acta_despacho_traslado(fecha)
#     elif tipo == "venta":
#         path = generar_acta_despacho_venta(fecha)
#     else:
#         return {"status": "error", "message": "Tipo de acta no válido"}

#     return FileResponse(path, media_type='application/pdf', filename=f"acta_{tipo}_{fecha}.pdf")


# from generador_pdf.pdf_generator import GeneradorPdfActa

# if __name__ == "__main__":
#     fecha = "2025-07-01"
#     generador = GeneradorPdfActa(fecha)
#     generador.generar_todos_los_pdfs()
