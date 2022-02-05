from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.expression import null, text
from sqlalchemy.orm import relationship

# importing our Base from database.py created with sqlalchemy 
from .database import Base

# define our ORM model for a post # it will create a table within a Postgres
class Post(Base):
    
    # how do we want to call this table
    __tablename__ = 'posts'
    
    # type of column we create
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    #creating relationship with our post database and users database by creating an owner_id column
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    #set up relationship to get owner's info # tell sqlalchemy to fetch owner's information based on relationship
    #class of another model # referencing class and not a table # it will create property for our post
    #when we retrieve a post it's going to return an owner property and figure out the relationship to a user
    #fetch a user based on owner id and return it to us
    owner = relationship("User") 
    

# we need to import models py into main file with the following line:
# from homedirectory import models.py
# from . import models

# USER ORM MODEL
class User(Base):
    __tablename__ = "users"
    
    # columns
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # optional for alembic testing
    phone_number = Column(String)


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)