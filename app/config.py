# env var
from pydantic import BaseSettings

# the goal of it is to verify if all environment variables are here
class Settings(BaseSettings):
    # list of the environment variables that need to be set as properties of the class itself 
    # perform all the validation 
    # best pracrice to have env var all caps # pydantic will fix it to upper_case
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    #import variables from a specific file
    class Config:
        env_file = ".env"
    

#pydantic will convert it to upper_case and validate if it's a string
settings = Settings() # instance of a settings class
#access variables
#print(settings.database_username)