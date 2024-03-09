from typing import List

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, Response, status

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
async def get_posts(
    db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)
):
    # cursor.execute("SELECT * FROM posts;")
    # posts = cursor.fetchall()
    print(current_user)
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    # cursor.execute("INSERT INTO posts ( title, content, published ) VALUES ( %s, %s, %s) RETURNING *;"
    #                ,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()

    # conn.commit()

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    # cursor.execute("SELECT * FROM posts WHERE id = %s;", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found!",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):

    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (id,))
    # post = cursor.fetchone()

    delete_post_query = db.query(models.Post).filter(models.Post.id == id)

    if delete_post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with this id: {id} is not found",
        )

    # conn.commit()
    delete_post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
async def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):

    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s
    #             WHERE id = %s RETURNING *;""",
    #     (post.title, post.content, post.published, id),
    # )

    # updated_post = cursor.fetchone()

    update_post_query = db.query(models.Post).filter(models.Post.id == id)

    if update_post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with this id: {id} is not found",
        )

    # conn.commit()

    update_post_query.update(post.model_dump())
    db.commit()
    return update_post_query.first()
