from pydantic import BaseModel, Field
from typing import Union, List


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool = True
    # TODO: Add this back after Alembic setup-> friends: List[int]

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class Friend(BaseModel):
    id: int
    sender: int
    receiver: int
    accepted: bool = False

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
