from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Union, List


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


class PinBase(BaseModel):
    session_start_time: datetime
    # current_members: List[int] = []
    location_long: float
    location_lat: float
    description: str

    class Config:
        orm_mode = True


class Pin(PinBase):
    id: int
    owner_id: int
    member_count: int = 1
    is_active: bool = True
    session_end_time: datetime = None


class User(UserBase):
    id: int
    is_active: bool = True
    friends: List[UserBase] = []
    pin: Pin
    pin_id: int


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
