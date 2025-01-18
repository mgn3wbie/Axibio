from fastapi import FastAPI
import requests
from database import Manager

app = FastAPI()



@app.get("/")
async def root():
    db_manager = Manager()
    print("Table logs exists ? " + str(db_manager.create_missing_tables()))
    return {"message": "Hello World"}


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