from fastapi import FastAPI

app = FastAPI()

@app.get("/api/v1/orders")
def get_orders():
    return [
        {"order_id": "O001", "item": "Laptop", "service": "Orders"},
        {"order_id": "O002", "item": "Mouse", "service": "Orders"},
    ]
