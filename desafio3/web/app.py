from fastapi import FastAPI, HTTPException
import psycopg2
import redis
import os
from datetime import datetime

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "db_name")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
CACHE_HOST = os.getenv("CACHE_HOST", "cache")

def get_db_status():
    """Tenta conectar ao PostgreSQL."""
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        conn.close()
        return "Conectado com sucesso ao PostgreSQL."
    except Exception as e:
        return f"Falha ao conectar ao PostgreSQL: {e}"

def get_cache_status():
    """Tenta conectar ao Redis."""
    try:
        r = redis.Redis(host=CACHE_HOST, port=6379)
        r.ping()
        r.set('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return f"Conectado com sucesso ao Redis. Valor salvo: {r.get('timestamp').decode()}"
    except Exception as e:
        return f"Falha ao conectar ao Redis: {e}"

@app.get("/")
def home():
    """Endpoint principal que verifica a saúde dos serviços dependentes."""
    db_status = get_db_status()
    cache_status = get_cache_status()
    
    return {
        "web_status": "Serviço Web rodando.",
        "db_check": db_status,
        "cache_check": cache_status,
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)