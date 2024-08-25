import uvicorn

from fastapi import FastAPI

import models
from database import engine
from router import auth, post, user, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"msg": "Hello!!"}

if __name__ == "__main__":
    uvicorn.run("main:app",host="localhost", port=8080)
