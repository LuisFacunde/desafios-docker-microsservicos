from fastapi import FastAPI

app = FastAPI()

@app.get("/api/v1/users")
def get_users():
    return [
        {"id": 101, "name": "Luis", "service": "Users"},
        {"id": 102, "name": "Facunde", "service": "Users"},
    ]
