from pydantic import BaseModel




class User(BaseModel):
    '''
    data model for user login and registration request.
    '''
    username: str
    password: str

    class Config:
        orm_mode = True


class Recipe(BaseModel):
    '''
    data model for recipe related request.
    '''
    title: str
    description: str
    ingredients: str
    instructions: str
