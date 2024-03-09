import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(dotenv_path="app/.env")


class Settings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


settings = Settings()
