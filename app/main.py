from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session


from . import models
from . import schemas
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password='1234567', cursor_factory=RealDictCursor)
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


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts;")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def createPost(post: schemas.Post, db: Session = Depends(get_db)):
    # cursor.execute("INSERT INTO posts ( title, content, published ) VALUES ( %s, %s, %s) RETURNING *;"
    #                ,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data ": new_post}


@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s;",(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id: {id} was not found!')
    return {"data": post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):

    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *;",(id,))
    post = cursor.fetchone()
    
    
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with this id: {id} is not found")
    
    conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: schemas.Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s 
                WHERE id = %s RETURNING *;""",
                (post.title, post.content, post.published, id))
    
    updated_post = cursor.fetchone()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with this id: {id} is not found")

    conn.commit()
    return {'Updated Post': updated_post}