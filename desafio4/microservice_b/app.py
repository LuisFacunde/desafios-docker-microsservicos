from fastapi import FastAPI, HTTPException
import requests
import os
from datetime import datetime

app = FastAPI()

MS_A_HOST = os.getenv("MS_A_HOST", "users-service") 
MS_A_HOST = os.getenv("MS_A_HOST", "users-service") 
MS_A_URL = f"http://{MS_A_HOST}:8000/users"

@app.get("/status")
def get_combined_data():
    """Consome o Serviço A e combina as informações."""
    
    try:
        response = requests.get(MS_A_URL, timeout=5)
        response.raise_for_status() # Lança exceção se o status for 4xx ou 5xx
        users_data = response.json().get("usuarios", [])
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consumir Microsserviço A: {e}")
        raise HTTPException(status_code=503, detail=f"Serviço A indisponível ou erro na comunicação: {e}")

    combined_info = []
    for user in users_data:
        combined_info.append(f"Usuário {user['nome']} ativo desde {user['cadastro']} (Processado em B)")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Microsserviço B (Consumer) processado.")
    
    return {
        "status": "Processamento concluído com sucesso",
        "timestamp_b": datetime.now().isoformat(),
        "info_combinada": combined_info
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)