from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_posts = [{"title": "First Title","content": "First content","id": 1},{"title": "Second Title","content": "Second content","id":2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: int | None = None


def find_post(id: int) -> dict|None:
    for post in my_posts:
        if post['id'] == id:
            return post
    return None

@app.get("/")
async def root():
    return {"msg": "Hello!!"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts")
async def createPost(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(1,1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/post/{id}")
async def get_post(id: int):
    return {"data": find_post(id)}