from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

@app.get("/")
async def home(request: Request):
    ip_cliente = request.client.host
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"[{agora}] Requisição recebida de: {ip_cliente}") 
    
    return {
        "mensagem": "Olá do Servidor FastAPI!",
        "timestamp": agora,
        "ip_cliente_requisitante": ip_cliente
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)