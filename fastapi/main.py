from fastapi import FastAPI
from database import Manager
from octave_api import fetch_all_events
from data_transform import process_octave_response_into_dict_list
from data_transform import turn_camel_to_snake_case_for_dicts
from models import Logs

app = FastAPI()

@app.get("/")
async def root():
    db_manager = Manager()

    db_manager.create_missing_tables()

    response = fetch_all_events()

    if response.status_code == 200:
        events_list = process_octave_response_into_dict_list(response.json())
        events_list = turn_camel_to_snake_case_for_dicts(events_list)
        db_manager.persist_items_from_model(events_list, Logs)
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
