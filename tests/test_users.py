import pytest
from app import schemas
#from .database import client, session

from jose import jwt
from app.config import settings

'''
#performing actions
#running our code
#making sure results are what we expect them to be
def test_root(client):
    #access to the db object -> session.query(models.Post)
    res = client.get("/", )
    #print <Response [200]> object
    #print(res)
    #print payload # {'message': 'hello world'}
    #print(res.json())
    #to grab message property # hello world
    #print(res.json().get('message'))
    #to test that a route actually works
    assert res.json().get('message') == "hello world"
    print(res.status_code)
    assert res.status_code == 200
'''

#test create_user from user.py functionality
def test_create_user(client): #client object refers to the client we get from this fixture
    #since we now send a request to create a user we need 
    #we have to send a data in a body
    #to send a data in a body 
    #schemas.UserCreate inside schemas.py we check what params and its email and a password
    res = client.post("/users/", json={"email": "hello126@gmail.com", "password": "password123"}) 
    #print(res.json())
    #create new pydantic model # to do validation for us
    new_user = schemas.UserOut(**res.json()) # it will check if we have three properties of exact type
    #we expect to match schemas.UserOut #id email created_at
    #assert res.json().get("email") == "hello125@gmail.com"
    assert new_user.email == "hello126@gmail.com"
    assert res.status_code == 201
    #we are using dev db for tests
    #create separate db for testing
    #it's very easy to override dependency in testing env
    #instead of db: Session = Depends(get_db) -> db: Session = Depends(get_test_db) 
    #function that returns test instance of our database

#test for login # it will be dependent on a client fixture
def test_login_user(test_user,client):
    #we send it as a body but as a form-data and not a regular body
    #to change it to a form data we change json -> data
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    #taking token from schemas.Token
    #spread **res.json()
    #get the token
    login_res = schemas.Token(**res.json())
    #validate the token # decode the token
    payload = jwt.decode(login_res.access_token, 
                        settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

#failed login
@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", 403),
    ("hello126@gmail.com", "wrongpassword", 403),
    ("wrong@gmail.com", "wrongpassword", 403),
    (None, "password123", 422), # schema validation #missing fields 
    ("hello126@gmail.com", None, 422) # schema validation #missing fields
])

def test_incorrect_login(email, password, status_code, client):
    res = client.post("/login", data={"username": email, "password": password})
    
    assert res.status_code == status_code
    
    #this line won't apply for test case with 422
    #assert res.json().get("detail") == "Invalid Credentials" #from auth.py file
    #test wrong email and wrong password

