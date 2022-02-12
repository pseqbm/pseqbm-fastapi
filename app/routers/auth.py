from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, oauth2, schemas, models, utils

router = APIRouter(tags=["Authentication"])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
    # instead of user_credentials: schemas.UserLogin
    # we create dependency with user_credentials: OAuth2PasswordRequestForm=Depends() after this response in postman will see data via body > form-data
    # {
    # "username" = "asdf",
    # "password" = "alsdjf"
    # } 
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # use verify function from utils.py # if hashed password from user matches the hashed password from the database
    # incorrect login
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token # create access_token # data = the data we want to put inside the payload
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # return token  
    return {"access_token": access_token, "token_type": "bearer"}