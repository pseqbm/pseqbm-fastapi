#how we deal with authentication when it comes to testing

#def get_all_posts(client, test_user):
#    client.post(login) # we login we get a token, when we get a token we make a request to posts

#set up a fixture that does it for us
#instead of making requests to our API I would like to import a method # oauth2 method for creating access token
#fake our own token
#inside conftest we create a new fixture token and authorized client
import pytest
from typing import List
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/") 
    #print(res.json())
    #take a list of dictionaries and convert it into schema models
    #do validation using schema
    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, res.json())
    #print(list(posts_map))
    posts_list = list(posts_map)
    print(posts_list)
    #print(res.json())
    assert len(res.json()) == len(test_posts)
    #print(posts)
    assert res.status_code == 200
    #check certain fields <> tests_post is a sqlalchemy model
    #add order by filter criteria
  
#unauthenticated user is not able to retrieve the post
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

#one post
def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

#post with an id that does not exist
def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/8888")
    assert res.status_code == 404

#get one post
def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    #print(res.json())
    #do validation
    post = schemas.PostOut(**res.json())
    # #class PostOut(BaseModel):
    #   Post: Post
    #   votes: int
    #TO GRAB THE INFO ABOUT THE POST WE NEED TO GO TO POST PROPERTY AND THEN GRAB THE FIELDS
    assert post.Post.id == test_posts[0].id
    #sqlalchemy model
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "#wesome new content", True),
    ("favorite pizza ya", "$wesome old content", False),
    ("awesome chicken w", "%wesome aged content", True)
    ])
#create post
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    # test_posts to see if we run in an issue if posts already exists # it's optional
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    #do some validation with pydantic model
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


#let's test if default value published: bool = True inside PostBase inside schemas.py
def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    # test_posts to see if we run in an issue if posts already exists # it's optional
    res = authorized_client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})
    #do some validation with pydantic model
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "arbitrary content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]

#test if we are not logged in
#unauthenticated user is not able to retrieve the post
def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})
    assert res.status_code == 401

#unauthorized user is trying to delete a post
def test_unauthorized_user_delete_Post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

#test valid deletion
def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    #fetch all posts again to verify that the total number of posts is one less
    assert res.status_code == 204

#delete non-existing post # id that does not exist
def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/8888888888")
    assert res.status_code == 404

#user tries to delete a post that is not theirs #owned by someone else
#we need to have more than one user in the database and we need to have posts owned by multiple users
#set up more than user use fixture -> test_user
def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

#update post
def test_update_post(authorized_client, test_user, test_posts):
    #define a dictionary with the values we want to update
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    #same as we do inside post.py response_model=schemas.Post we can validate on our end on test as well
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

#update another user's post
def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    #update last post
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

#unauthorized user is trying to update the post
def test_unauthorized_user_update_Post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

#update the post the post that does not exist
def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    #it tries to validate it so we need to provide some data
    res = authorized_client.put(f"/posts/8888888888", json=data) #json=data will prevent us from getting validation errors
    assert res.status_code == 404


