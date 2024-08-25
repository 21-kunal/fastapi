from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status

import database, models, oauth2, schemas

router = APIRouter(prefix="/votes", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    request: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == request.post_id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with this id: {request.post_id} is not found",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id, models.Vote.post_id == request.post_id
    )
    found_vote = vote_query.first()

    if request.dir:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on the post {request.post_id}",
            )
        else:
            new_vote = models.Vote(post_id=request.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "Voted successfully"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist."
            )
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Vote deleted successfully"}
