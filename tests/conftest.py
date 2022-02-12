# this module represents creating users and getting user profile information
from fastapi.testclient import TestClient
# import our app instance from main.py file so we can test it
from app.main import app # app instance
#import schema
from app import schemas
#to use fixtures
import pytest

#sqlalchemy code
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base

from app.oauth2 import create_access_token

#used for posts
from app import models

#alembic option of creating db
#from alembic import command
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost:5432/fastapi_test"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

'''
#this will tell sqlalchemy to build all tables without alembic
#when running first test it will create all tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
'''

#set our TestClient to client variable
#to generate requests we will use client
#client = TestClient(app)
#logic to delete and create tables # logic related to db
@pytest.fixture(scope="function")
#scope="function" run fixture for every single function that requests this fixture
def session():
    print("my session fixture ran")
    #run our code after our test finishes
    #after code runs we want drop table
    #clear out anything we had previously # clear out our tables 
    #in this order with #pytest --disable-warnings -v -x 
    #we will see what was the current state of our tables when the test crashed
    Base.metadata.drop_all(bind=engine)
    #run our code before we run our test
    #before code runs we can create tables
    Base.metadata.create_all(bind=engine)
    #alembic option of creating db
    #build out all tables
    #command.upgrade("head")
    #this session fixture will yield the db object #to query fields
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#to get around limitation related to unique constraint in db post we can use fixtures
@pytest.fixture(scope="function")
#by passing session object inside our client object
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    #do override for db
    app.dependency_overrides[get_db] = override_get_db
    #return brand new test client
    yield TestClient(app) #yield is the same as return 
    #keep the table after it's done
    #alembic option of creating db
    #build out all tables
    #command.downgrade("base")

#for our test_post.py def test_delete_other_user_post
@pytest.fixture
#creating a test user
def test_user2(client):
    user_data = {"email": "olla123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    #return information about the user
    #print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    #print(res.json())
    return new_user

#create a fixture to create a user
@pytest.fixture
#creating a test user
def test_user(client):
    user_data = {"email": "hello126@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    #return information about the user
    #print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    #print(res.json())
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})
#for authorized path client we will use authorized client

@pytest.fixture
def authorized_client(client, token):
    #update the headers
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    #getting the original client adding specific header that we get from the token fixture and returing client back
    return client 

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "1st title",
        "content": "1st content",
        "owner_id": test_user["id"]
    },
    {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user["id"]
    },
    {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user["id"]
    },
    {
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_user2["id"]
    }]
    
    #take a dictionary and convert it into a post models use map function
    #map(function, post_data)
    
    def create_post_model(post):
        #convert dictionary into a post model
        return models.Post(**post)
    
    #convert to a user model, returns a map
    post_map = map(create_post_model, posts_data)
    #convert to a list
    posts = list(post_map)
    session.add_all(posts)
    
    #sqlalchemy method add_all
    #session.add_all([models.Post(title="1st title", content="1st content", owner_id=test_user["id"]),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user["id"]),
    #                 models.Post(title="3rd title", content="3rd content", owner_id=test_user["id"])])

    session.commit()

    posts = session.query(models.Post).all()
    return posts

