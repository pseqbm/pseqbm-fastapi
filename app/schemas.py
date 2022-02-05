from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
'''
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True

class UpdatePost(BaseModel):
    #title: str
    #content: str
    published: bool # there won't be a default value for published because we want them explicitly provide each column
'''

# REQUEST -> USER SENDING DATA TO US
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# response after the user was created without the password included
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    # converting sqlalchemy model to our pydantic model
    class Config:
        orm_mode = True

# RESPONSE US SENDING DATA TO USER # POST OUT
class Post(PostBase):
    id: int
    created_at: datetime
    # we have not added it in the PostBase and PostCreate cause we don't want to require it from a user
    # let the logic from our route grab the id from the token and then use it as the field # we won't use it as a body
    owner_id: int
    #return pydantic model UserOut # used for owner retrieval info # in models.py set up relationship
    owner: UserOut
    # convert sqlalchemy model into pydantic model # it will tell pydantic ignore the fact it's not a dictionary and simply convert it into a dictionary
    class Config:
        orm_mode = True

# udpate schema response after votes query inside get_posts path function
class PostOut(BaseModel):
    Post: Post
    votes: int
    # convert sqlalchemy model into pydantic model # it will tell pydantic ignore the fact it's not a dictionary and simply convert it into a dictionary
    class Config:
        orm_mode = True

#https://pydantic-docs.helpmanual.io/usage/types/
# pip install email-validator # EmailStr
# request to create user 
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
# define schema for user credentials
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# define schema for a token
class Token(BaseModel):
    access_token: str
    token_type: str

# schema for token data 
class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # less than equal to 1 will be allowed


    