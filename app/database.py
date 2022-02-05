# It will handle our database connection
# sql welcoming code that we want
# https://fastapi.tiangolo.com/tutorial/sql-databases/
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# transferred from main.py 
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time 

from .config import settings

# connection string // where is our postgres database located'
                         #'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# create an engine # engine is responsible for SQLALCHEMY to connect to POSTGRESQL DATABASE
# the engine is responsible for establishing that connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# to talk to a db we need to make a use of session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # default values

# in case we use sqllite:
'''
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
'''

# all of the models we will define will extend this base class:
Base = declarative_base()

# Dependency # it should imported in our main file
# Session Object is what responsible for talking with db # get connection or a session to a database # once the request is done close it out
# it will create a session towards our database for every request to that specific api point
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
# postgres driver extracted from main.py # we can delete this, we use sqlalchemy, but for documentation purposes we will use it
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password='password', cursor_factory=RealDictCursor) #host api address, database, user, password # cursor_factory will give us a column name
        cursor = conn.cursor()
        print("Database connections was successful!")
        break
    except Exception as error: 
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)
'''
