from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Union, List, Type

# Forward Declaration to solve circular dependency
User = None
Pin = None


class UserBase(BaseModel):
    email: str
    name: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class Friend(BaseModel):
    id: int
    sender: int
    receiver: int
    accepted: bool = False

    class Config:
        orm_mode = True


class PinCreate(BaseModel):

    location_long: float
    location_lat: float
    description: str

    class Config:
        orm_mode = True


class Pin(PinCreate):
    id: int
    owner_id: int
    joiner_list: List[int] = []
    is_active: bool = True
    session_start_time: datetime = datetime.utcnow()
    session_end_time: datetime = None


class User(UserBase):
    id: int
    is_active: bool = True
    friends: List[UserBase] = []
    pin_id: int = None
    joined_pin_id: int = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
