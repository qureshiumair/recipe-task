from sqlalchemy import Column, Integer, String, Sequence, Text, ForeignKey

from .database import Base

class Users(Base):
    '''
    user model to store user information in the database.
    '''
    __tablename__ = "user_table"
    id = Column(Integer, Sequence('item_id_seq', start=1000),
                primary_key=True)
    username = Column(String,nullable=False,unique=True)
    hash_password = Column(String,nullable=False)


class Recipes(Base):
    '''
    recipe model to store recipe information in the database.
    '''
    __tablename__ = "recipe_table"
    id = Column(Integer, Sequence('item_id_seq', start=2000),
                primary_key=True)
    title = Column(String,nullable=False,unique=True)
    description = Column(Text)
    ingredients = Column(Text)
    instructions = Column(Text)
    created_by = Column(String, ForeignKey("user_table.username"))
