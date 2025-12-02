from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

USERS_DATA = [
    {"id": 1, "nome": "João Silva", "cadastro": "2024-01-10"},
    {"id": 2, "nome": "Maria Santos", "cadastro": "2024-03-25"},
    {"id": 3, "nome": "Pedro Oliveira", "cadastro": "2024-05-18"},
]

@app.get("/users")
def get_users():
    """Endpoint que retorna a lista de usuários."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Microsserviço A (Users) requisitado.")
    return {"usuarios": USERS_DATA}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)