from pydantic import BaseModel, Field
from typing import Union


class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(default=None, title="The description of the item")
    price: float
    tax: Union[float, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
