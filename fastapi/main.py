from fastapi import FastAPI
import requests
import db_manager
import os

app = FastAPI()

db_manager.create_missing_db_elements()

@app.get("/")
async def root():
    return {"message": "Hello World", "user" : os.getenv("POSTGRES_USER"), "password" : os.getenv("POSTGRES_PASSWORD")}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/fetch_data")
async def fetch_data():
    api_url = "https://octave-api.sierrawireless.io/v5.0/axibio/event?path=/axibio/devices/gaiabox_005/eventlog"
    headers = {"X-Auth-token": "7WtXx1NeizYcwuyVHzfXxTZXDhQnDy2Z", "X-Auth-User": "guest_axibio"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}