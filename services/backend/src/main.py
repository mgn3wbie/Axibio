from fastapi import FastAPI
from src.api.octave_api import fetch_all_events
from src.db.database import Manager
import src.utils.data_transform as data
import src.db.models as models

app = FastAPI()

@app.get("/")
async def root():
    db_manager = Manager()

    db_manager.create_missing_tables()

    response = fetch_all_events()

    if response.status_code == 200:
        events_list = data.process_octave_response_into_dict_list(response.json())
        events_list = data.turn_camel_to_snake_case_for_dicts(events_list)
        db_manager.persist_items_from_model(events_list, models.Logs)
        
        energy_events_results = db_manager.get_all_events_with_name("energy_inc")
        events = []
        for id, event_data in energy_events_results:

            result = data.flatten_dict_depth(event_data)
            result.update({"id": id, "name": "energy_inc"})
            events.append(result)
        events = data.turn_camel_to_snake_case_for_dicts(events)
        db_manager.persist_items_from_model(events, models.Event)


        return response.json()
    else:
        return {"error": "Failed to fetch data"}
