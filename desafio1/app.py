from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

@app.get("/")
async def read_root(request: Request):
    ip_cliente = request.client.host
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_msg = f"[{agora}] Requisição recebida de: {ip_cliente}"
    
    print(log_msg) 
    
    return {
        "mensagem": "Olá do Servidor FastAPI!",
        "timestamp": agora,
        "ip_cliente_requisitante": ip_cliente
    }