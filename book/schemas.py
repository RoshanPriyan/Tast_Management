from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    description: str
    author: str
    count: int


class BorrowBookSchema(BaseModel):
    pass