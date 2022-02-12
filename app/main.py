#“uvicorn ERROR: [Errno 98] Address already in use” Code Answer
#find the process using the port
#lsof -i :8000
#and kill it
#kill -9 process_id
# @ decorator
# .get # HTTP method
# ('/') path or root url

#from typing import Optional, List
from fastapi import FastAPI #, Response, status, HTTPException, Depends
#from fastapi.params import Body
#from pydantic import BaseModel
#from passlib.context import CryptContext
#from random import randrange
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time 
from . import models #, schemas, utils 
#import from a database.py import right commands for models.Base.metadata.create_all(bind=engine)
from .database import Base, engine #, SessionLocal, get_db
# import from routers folder post.py, user.py
from .routers import post, user, auth, vote
from .config import settings

from fastapi.middleware.cors import CORSMiddleware

#it will create all our models (taken from https://fastapi.tiangolo.com/tutorial/sql-databases/) # it will create a table within postgresql
#first check if the table exists if not, it will create it based on rules described in models.py
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#list of urls/domains that can talk to our API
#["*"] every single API 
# we need strict list of domains/origins
#origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"]

#CORS
app.add_middleware(
    CORSMiddleware, # middleware is bascially a function that runs before any request
    allow_origins=origins, # specify what domains should be available to talk to our API
    allow_credentials=True,
    allow_methods=["*"], # allow specific HTTP methods
    allow_headers=["*"], # allow specific headers
)

#schema model for our incoming posts should be here but we removed it to its own file schemas.py

'''
class UpdatePost:
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
'''

#in memory posts # until db created in this tutorial
#my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}, {"title":"favorite foods", "content":"I like pizza", "id": 2}]
'''
def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i 
'''

#to connect routers to our files inside the routers folder
#include everything from post.py router 
#it finds a match it responds accordingly
app.include_router(post.router)
#include everything from user.py router  
#grabbing router object from a user file and include it inside our app routes
app.include_router(user.router)
#auth route for user login stored in auth.py
app.include_router(auth.router)

app.include_router(vote.router)

#path operation or route operation
#decorator @ reference fast api instance and use a method
#function to perform async tasks # path operation functions make as much descriptive # async (optional) # path operation function

@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"} # data sent back to a user
