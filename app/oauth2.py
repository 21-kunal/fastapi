from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException, status

from . import database, models, schemas
from .config import settings

oauth_schema = OAuth2PasswordBearer(tokenUrl="login")

ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def create_access_token(data: dict):

    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration})

    new_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return new_token


def verify_access_token(token: str, credentials_exception):

    try:
        pay_load = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = pay_load.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth_schema), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
