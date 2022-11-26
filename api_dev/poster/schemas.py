from pydantic import BaseModel
from typing import Union


class ImagePost(BaseModel):
    caption: Union[str, None] = None
    location: str
    date_time: str
    username: str