#import status, HTTPException, Depends, APIRouter from fastapi library
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
#import session from sqlalchemy 
from sqlalchemy.orm import Session
#from homedirectory/routers import models.py and schemas.py # one dot for current directory, two dots to go upper directory to get models.py and schemas.py
from .. import models, schemas, utils 
#import from a database import right commands for models.Base.metadata.create_all(bind=engine)
from ..database import engine, SessionLocal, get_db
#import router object
router = APIRouter(
    prefix="/users",
    #grouping requests into categories
    tags=["Users"]
)

#create user # post request to url of users
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)): # email and address from user will be stored inside the variabl user and will be pydantic object
    #before we create a user we need to create a hash to a password
    #hash the password - user.password # can be stored within user
    #hashed_password = pwd_context.hash(user.password)
    #after placing this function inside utils.py 
    hashed_password = utils.hash(user.password)
    #update pydantic user model with the hashed password
    user.password = hashed_password
    #take a user from our front end, convert it to a dictionary, unpack it from a dictionary and store it according to our User model in a new_user variable
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    #refresh db to see a brand new user
    db.refresh(new_user)
    return new_user


#get user based on the user id
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user