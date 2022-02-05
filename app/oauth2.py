from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


from .config import settings

#tokenUrl is endpoint to our login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY RESIDES ON OUR SERVER ONLY
#ALGORITHM WE WILL USE HS256
#EXPIRATION OF THE TOKEN / HOW LONG USER WILL LOG IN BEFORE IT WIL HIT THE EXPIRATION # EXPIRATION TIME

#to get a string like this run:
#openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes # 60 minutes # user is logged in for a certain amount of time

#access token will have a payload data
def create_access_token(data: dict):
    to_encode = data.copy()
    #grab the current time and add the current minutes # utcnow() to avoid expiration error
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #taking copy of a dictionary, update it with the expiration info
    to_encode.update({"exp": expire})
    #from jose library, creating jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # algorithms=[ALGORITHM] it expects a list of algorithms
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        # validate our specific token schema
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    #make use of that data # in our case it is just an id
    return token_data

#we can pass this as a dependency in any of our path operations 
#take a token from a request automatically # extract id # verify if token is valid # fetch a user from a db and add as a paremeter to our path operation
#fetch user from a database attach a user to any path operation and perform any necessary logic for this user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
