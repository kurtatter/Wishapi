from pydantic import BaseModel, HttpUrl
from typing import Optional

from datetime import date


class WishBase(BaseModel):
    date: date
    title: str
    url: HttpUrl
    price: float
    description: Optional[str]


class Wish(WishBase):
    id: int

    class Config:
        orm_mode = True


class WishCreate(WishBase):
    pass


class WishUpdate(WishBase):
    pass
