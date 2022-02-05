from passlib.context import CryptContext

#password hashing related line of code
#we are telling passlib what is the default hashing algorithm # bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#hashing password
def hash(password: str):
    return pwd_context.hash(password)

# take raw password # hash it for us # compare the hash to our hashed password in the database # used in auth.py
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

 

