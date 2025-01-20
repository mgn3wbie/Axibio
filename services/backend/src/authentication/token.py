from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError
import jwt

from datetime import datetime, timedelta, timezone
from typing import Annotated
import os

from src.db.database import DBManager
from src.authentication.password import verify_password
import src.db.models as models

# secret key provided from .env
SECRET_KEY = os.environ["SECRET_KEY_JWT"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# dependency injection
oauth_token = Annotated[str, Depends(oauth2_scheme)]

class User(BaseModel):
    username: str
    disabled: bool | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: oauth_token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    db_user = DBManager.get_user_for_email(token_data.username)
    user = User(username=db_user.email, disabled=db_user.disabled) if db_user else None
    if user is None:
        raise credentials_exception
    return user

def authenticate_user(username: str, password: str):
    user: models.User = DBManager.get_user_for_email(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return User(username=user.email, disabled=user.disabled)

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user