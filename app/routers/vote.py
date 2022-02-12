from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
# vote: schemas.Vote -> expecting a user to provide some data in a body we need to define a schema Vote
# db: Session = Depends(database.get_db) -> set up database so we can make queries
# current_user: int = Depends(oauth2.get_current_user) -> allow to vote only authorized users
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # check if post exists before making a vote
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")
 
    #create a vote # query if the vote already exist #if already a vote for this specific post_id # second check # check if this specific user voted or liked this post already
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
     
    #if the user wants like a post but we already found a post, it means he already liked this specific post and can't like it anymore
    found_vote = vote_query.first()
    
    # find the user id of the post
    # compare it to the current user
    # if it is the same raise exception he can't vote on his own posts
    if post.owner_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} can not vote on his own post with {vote.post_id}")

    # when the vote direction is one
    if (vote.dir == 1):
        # if we found a vote
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post with {vote.post_id}")
        # if we didn't find a vote create a brand new Vote
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        # if user provide direction of 0 - they want to delete a vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exists")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"successfully deleted vote"}


