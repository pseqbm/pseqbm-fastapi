#import status, HTTPException, Depends, APIRouter from fastapi library
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
#import session from sqlalchemy 
from sqlalchemy.orm import Session
#from homedirectory/routers import models.py and schemas.py # one dot for current directory, two dots to go upper directory to get models.py and schemas.py
from .. import models, schemas, oauth2
#import from a database import right commands for models.Base.metadata.create_all(bind=engine)
from ..database import engine, SessionLocal, get_db
#being able to convert bunch of schemas list objects into a list of posts
from typing import Optional, List
#it will give us access to functions like count
from sqlalchemy import func 
#import router object
#to avoid repetition inside our paths get("/posts") get("/posts/{id}") etc. 
#we can pass in parameter to APIRouter method
router = APIRouter(
    prefix="/posts", #+ #/id / posts/{id}
    # adding group name to group everything in fastapi docs with this link http://127.0.0.1:8000/docs
    tags=['Posts']
)


''''
@app.get('/sqlalchemy') # import Session from sqlalchemy and import Depends from FastApi library
# anytime we want make database operation with sqlalchemy within our FastApi application we want to pass db: Session = Depends(get_db) as a parameter within our path function
# store it inside db variable
# call Session object
# call get_db function within Depends object to make a dependency
def test_posts(db: Session = Depends(get_db)):
    #SQLALCHEMY CODE
    # db object query method Post model represents a table # fetch all posts from our model
    posts = db.query(models.Post).all() # without .all() it will print sql command
    #SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at FROM posts
    return {"data": posts}
'''


#retrieve posts
#@router.get("/")
@router.get("/", response_model=List[schemas.PostOut]) # pydantic data type validation is happening because we use response_model=List[schemas.Post]
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    #SQL CODE
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    
    #SQLALCHEMY CODE
    #posts = db.query(models.Post).all()
    #print(current_user.id)
    # print(limit)
    #all posts are public 
    #{{URL}}posts?limit=2&skip=2&search=something%20beaches
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # -> to make all posts non-public and get_posts only logged in user owns
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #COUNT VOTES WITH SQLALCHEMY
    #.join by default is left inner
    #SELECT posts.*, COUNT(votes.post_id) as votes FROM posts LEFT INNER JOIN votes ON posts.id = votes.post_id WHERE posts.id = 10 group by posts.id;
    #SELECT posts.*, COUNT(votes.post_id) as votes FROM posts LEFT OUTER JOIN votes ON posts.id = votes.post_id WHERE posts.id = 10 group by posts.id;
    #models.Vote - the table we join with Post
    #models.Vote.post_id - the column
    #models.Post.id - the column
    #isouter=True
    #group_by(models.Post.id)
    #perform a count -> from sqlalchemy import func
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)
    #print(posts)
    return posts


#create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # oauth2.get_current_user is what forces to be logged in before anything else happens
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #(payload:dict=Body(...)): #print(post) # pydantic model #print(post.dict()) # convert pydantic model into regular python dictionary
    #SQL CODE
    #SQL injection can be made if instead of %s post.title, post.content, post.published used
    #cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published}))
    #we don't want to do string interpolation # we are going to parematirize, or sanitize inputs # postgress will make sure there is no malicious sql commands/injections
    #staged data
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #saved data or persist it to database
    #conn.commit()

    #PRIOR SQL CODE
    #post_dict = post.dict()
    #post_dict["id"] = randrange(0, 1000000)
    #my_posts.append(post_dict)

    #SQLALCHEMY CODE
    #create an entry
    #we have access to an object post , which is pydantic model and matches the schema
    #post.dict() #convert to a regular dictionary
    #take dictionary and convert it to this format title=post.title, content=post.content, published=post.published 
    #to do it we use ** to unpack the dictionary
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # with owner_id=current_user.id we are spreading out a schema that we get from a body
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #get it pushed to a database similar to conn.commit()
    db.add(new_post)
    db.commit()
    #returning statement in sqlalchemy # retrieve new post we just created and store it back in a variable new_post
    db.refresh(new_post)
    return new_post


#get post
@router.get("/{id}", response_model=schemas.PostOut) # {id} path parameter # fastapi will extract id and we will pass it to our functionality # path parameter will always be returned as a string, we need to convert it into int
#def get_post(id: int, response: Response):
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # int will make sure it's converted #print(type(id))
    #SQL CODE
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),)) # extra comma at the end can solve some potential issues
    #post = cursor.fetchone()
    
    #PRIOR SQL CODE
    #print(test_post)
    #post = find_posts(id)

    #SQLALCHEMY CODE
    #id from each model post is compared to id from path parameter {id} that user inputs on front end
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    #with votes count per post
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    #print(post)
    #SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at FROM posts 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    #all posts are public -> to make all posts non-public and get_post only logged in user owns
    #if post.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    #print(post)
    return post


#delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    #SQL CODE
    #deleting post 
    #cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    
    #PRIOR SQL CODE
    #find the index in the array that has required ID # my_posts.pop(index)
    #index = find_index_post(id)
    #index changed on deleted_post
    
    #SQLALCHEMY CODE
    #save query
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    #my_posts.pop(index)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) # {"message":"post was succesfully deleted"}


#update post
@router.put("/{id}", response_model=schemas.Post)
#def update_post(id: int, post: Post): # post variable Post schema # all the data we recieve from the front end
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    #updated_post
    #SQL CODE 
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published= %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    #PRIOR SQL CODE
    #index = find_index_post(id)
    #index changed into updated_post
    
    #convert to a regular python dictionary 
    #post_dict = post.dict()
    #add the id so this final dictionary has built in
    #post_dict["id"] = id
    #for the post within index we are going to replace it with post_dict
    #my_posts[index] = post_dict
    #post_dict change on updated_post

    #SQLALCHEMY CODE
    #saving query
    post_query = db.query(models.Post).filter(models.Post.id == id) 
    #running query
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    #chaining our previous query with the update query
    #post_query.update({"title": "hard coded", "content": "hard coded"}, synchronize_session=False)
    #post.dict() fields we want to update
    #updated_post.dict() works only for pydantic model it does not work for our sqlmodel
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    #returning updated post to the user
    return post_query.first()

