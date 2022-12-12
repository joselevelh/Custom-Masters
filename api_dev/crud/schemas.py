from pydantic import BaseModel, Field
from typing import Union


class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(default=None, title="The description of the item")
    price: float
    tax: Union[float, None] = None