from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pyodbc
import pandas as pd
from langchain_ollama import OllamaLLM
import datetime

app = FastAPI(title="Joyart AI API")

# Para que el index.html pueda hablar con el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# CAMBIA ESTA PASS SI QUIERES
DB_CONN = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=200.2.250.58;DATABASE=joyart_prueba;UID=sa;PWD=d@,.-20p03r1'

class PreguntaIA(BaseModel):
    pregunta: str

class Lead(BaseModel):
    email: str

# 1. BOTON CRM DEMO
@app.get("/api/crm/demo")
def crm_demo():
    hoy = datetime.date.today()
    return {"mensaje": "CRM Joyart conectado 🔥", "fecha": str(hoy), "leads_nuevos": 12}

# 2. CHAT IA
@app.post("/api/chat-ia")
def chat_ia(data: PreguntaIA):
    esquema = "TABLA Articulo: IdArticulo, Codigo, ValorVenta. TABLA Cliente: rutCliente, primerNombre, correoCliente"
    llm = OllamaLLM(model="llama3")
    prompt = f"Eres DBA SQL Server. Responde SOLO con SELECT. ESQUEMA: {esquema}. Pregunta: {data.pregunta} SQL:"
    sql_generado = llm.invoke(prompt).strip().replace("```sql","").replace("```","")
    
    conn = pyodbc.connect(DB_CONN)
    df = pd.read_sql(sql_generado, conn)
    conn.close()
    return {"sql": sql_generado, "datos": df.to_dict(orient='records')}

# 3. GUARDAR LEAD
@app.post("/api/lead")
def guardar_lead(lead: Lead):
    # Por ahora solo devuelve ok. Despues lo conectamos a la BD
    return {"status": "Lead guardado", "email": lead.email}