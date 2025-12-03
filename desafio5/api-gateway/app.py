from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

USERS_URL = "http://users-service:8000/api/v1"
ORDERS_URL = "http://orders-service:8000/api/v1"

def forward_request(base_url: str, path: str):
    url = f"{base_url}{path}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar backend {base_url}: {e}")
        raise HTTPException(status_code=503, detail=f"Serviço indisponível ou erro: {e}")

@app.get("/users")
def route_users():
    return forward_request(USERS_URL, "/users")

@app.get("/orders")
def route_orders():
    return forward_request(ORDERS_URL, "/orders")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)