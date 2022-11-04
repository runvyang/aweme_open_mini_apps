
from fastapi import FastAPI

app = FastAPI()

@app.get("/v1/ping")
def ping():
    return "pong"

@app.get("/items")
def get_item_list():
    # todo
    return []

@app.get("/items/{item_id}")
def get_item(item_id):
    return {}
