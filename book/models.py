from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base


class BookModel(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(500), unique=True, nullable=False)
    description = Column(String(500), nullable=False)
    author = Column(String(100), nullable=False)
    count = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    available_count = Column(Integer, nullable=True)

    borrowed_books = relationship("BorrowBookModel", back_populates="book")


class BorrowBookModel(Base):
    __tablename__ = "borrowed_books"

    STATUS = ["BORROWED", "RETURNED"]

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    borrow_date = Column(TIMESTAMP, server_default=func.current_timestamp())
    return_date = Column(TIMESTAMP, nullable=True)
    status = Column(String, nullable=False)

    book = relationship("BookModel", back_populates="borrowed_books")
