from typing import Annotated
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.octave_api import fetch_all_events
from src.db.database import DBManager
import src.utils.data_transform as data
import src.auth.auth_process as auth
import src.db.models as models


app = FastAPI()

@app.post("/signin")
async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> auth.Token:
    if form_data.username.endswith("@axibio.com") and DBManager.get_user_for_email(form_data.username) is None:
        user_model = models.User(email=form_data.username, hashed_password=auth.get_password_hash(form_data.password), disabled=False)
        DBManager.persist_item(user_model)
    

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> auth.Token:
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return auth.Token(access_token=access_token, token_type="bearer")

oauth_current_user = Annotated[auth.User, Depends(auth.get_current_active_user)]

@app.get("/users/me/", response_model=auth.User)
async def read_users_me(
    current_user: Annotated[auth.User, Depends(auth.get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[auth.User, Depends(auth.get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]



@app.get("/")
async def root():


    DBManager.create_missing_tables()

    DBManager.create_fake_users()

    response = fetch_all_events()

    if response.status_code == 200:
        events_list = data.process_octave_response_into_dict_list(response.json())
        events_list = data.turn_camel_to_snake_case_for_dicts(events_list)
        DBManager.persist_dicts_from_model(events_list, models.Logs)
        
        energy_events_results = DBManager.get_all_events_with_name("energy_inc")
        events = []
        for id, event_data in energy_events_results:

            result = data.flatten_dict_depth(event_data)
            result.update({"id": id, "name": "energy_inc"})
            events.append(result)
        events = data.turn_camel_to_snake_case_for_dicts(events)
        DBManager.persist_dicts_from_model(events, models.Event)


        return response.json()
    else:
        return {"error": "Failed to fetch data"}
