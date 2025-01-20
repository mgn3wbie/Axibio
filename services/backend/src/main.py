from typing import Annotated
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.authentication.token import Token, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user
from src.api.octave_api import fetch_all_events
from src.db.database import DBManager
import src.utils.data_transform as data
import src.db.models as models
from src.authentication.token import User, authenticate_user
from src.authentication.password import get_password_hash


oauth_current_user = Annotated[User, Depends(get_current_active_user)]
DBManager.create_missing_tables()

app = FastAPI()

@app.post("/signin")
async def signin_for_new_user(
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


@app.post("/token")
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
    return Token(access_token=access_token, token_type="bearer")

# todo : find a way to disconnect a user
@app.post("/logout")
async def logout() -> Token:
    return Token(access_token="", token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: oauth_current_user,
):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(
    current_user: oauth_current_user,
):
    return [{"item_id": "Foo", "owner": current_user.username}]



@app.get("/fetch_data")
async def root():
    response = fetch_all_events()

    if response.status_code == 200:
        events_list = data.process_octave_response_into_dict_list(response.json())
        events_list = data.turn_camel_to_snake_case_for_dicts(events_list)
        DBManager.add_or_update_dicts_from_model_with_ids(events_list, models.Logs)
        
        energy_events_results = DBManager.get_all_events_with_name("energy_inc")
        events = []
        for id, event_data in energy_events_results:

            result = data.flatten_dict_depth(event_data)
            result.update({"id": id, "name": "energy_inc"})
            events.append(result)
        events = data.turn_camel_to_snake_case_for_dicts(events)
        DBManager.add_or_update_dicts_from_model_with_ids(events, models.Event)


        return response.json()
    else:
        return {"error": "Failed to fetch data"}
