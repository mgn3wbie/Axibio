from typing import Annotated
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

import src.api.octave_api as octave_api
from src.db.database import DBManager
from src.auth.auth_process import *
import src.utils.data_transform as data
import src.db.models as models
import os

DBManager.create_missing_tables()
oauth_current_user = Annotated[User, Depends(get_current_active_user)]

app = FastAPI()

# middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ["FRONTEND_URL"]],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def homepage():
    return {"message": "Welcome to the homepage"}

@app.post("/register")
async def register_new_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = models.User(email=form_data.username, hashed_password=get_password_hash(form_data.password), disabled=False)
    # only create user if axibio and not already created
    # todo : use an email to generate password
    if user.email.endswith("@axibio.com") and DBManager.get_user_for_email(user.email) is None:
        DBManager.add_item_if_doesnt_exist(user, "email")
        return await login_for_access_token(form_data)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Either you are not allowed to register to this platform, or you already have an account",
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="Bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: oauth_current_user,
):
    return current_user


@app.post("/data/refresh")
async def data_refresh(
    current_user: oauth_current_user,
):
    response = octave_api.fetch_all_events()

    if response.status_code == 200:
        events_list = data.process_octave_response_into_dict_list(response.json())
        events_list = data.turn_camel_to_snake_case_for_dicts(events_list)
        DBManager.add_or_update_dicts_from_model_with_ids(events_list, models.Logs)

        energy_events_results = DBManager.get_all_logs_with_event_name("energy_inc")
        events = data.turn_logs_into_energy_events(energy_events_results)
        DBManager.add_or_update_dicts_from_model_with_ids(events, models.Event)
        return {"message": "succesfully refreshed data"}
    else:
        return {"error": "Failed to refresh data"}

# TODO: handle errors from db fetch
@app.get("/data/events")
async def get_events(
    current_user: oauth_current_user,
):
    results = DBManager.get_all_energy_events()
    json_events = data.turn_energy_events_query_results_into_json(results)
    return json_events
