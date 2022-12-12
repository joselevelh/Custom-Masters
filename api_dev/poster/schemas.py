from pydantic import BaseModel
from typing import Union


class ImagePost(BaseModel):
    caption: Union[str, None] = None
    location: str
    date_time: str
    username: str


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
