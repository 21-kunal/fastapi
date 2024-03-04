from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='1234567', cursor_factory=RealDictCursor)
        # RealDictCursor give the columns name with the returned rows
        cursor = conn.cursor()
        print("Successfully connected to Database")
        break
    except Exception as e:
        print(f"Error connecting to database: {e}")
        time.sleep(2)


my_posts = [{"title": "First Title","content": "First content","id": 1},{"title": "Second Title","content": "Second content","id":2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = False


def find_post(id: int) -> dict|None:
    for post in my_posts:
        if post['id'] == id:
            return post
    return None


def find_ind(id: int) -> int|None:
    for ind, post in enumerate(my_posts):
        if post['id'] == id:
            return ind
    return None


@app.get("/")
async def root():
    return {"msg": "Hello!!"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def createPost(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(1,1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id: {id} was not found!')
    return {"data": post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    ind = find_ind(id)

    if ind == None:
        print(ind)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with this id: {id} is not found")
    
    my_posts.pop(ind)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    ind = find_ind(id)

    if ind == None:
        print(ind)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with this id: {id} is not found")
    
    updated_post = post.model_dump()
    updated_post['id'] = id
    my_posts[ind] = updated_post

    return {'Updated Post': updated_post}