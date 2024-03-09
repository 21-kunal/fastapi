import time
from typing import List

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, Response, status

from . import models, schemas, utils
from .database import engine, get_db
from .router import auth, post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="1234567",
            cursor_factory=RealDictCursor,
        )
        # RealDictCursor give the columns name with the returned rows
        cursor = conn.cursor()
        print("Successfully connected to Database")
        break
    except Exception as e:
        print(f"Error connecting to database: {e}")
        time.sleep(2)


@app.get("/")
async def root():
    return {"msg": "Hello!!"}
