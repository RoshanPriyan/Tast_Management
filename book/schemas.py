from pydantic import BaseModel
from typing import Optional


class BookSchema(BaseModel):
    title: str
    description: str
    author: str
    count: int
