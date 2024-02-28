from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
async def root():
    return {"msg": "Hello!!"}

@app.get("/posts")
async def get_posts():
    return {"data": "This is a post"}

@app.post("/createPost")
async def createPost(payLoad: dict = Body(...)):
    print(payLoad)
    return {"msg": payLoad}