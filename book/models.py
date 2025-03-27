from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class BookModel(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(String(500), nullable=False)
    author = Column(String(100), nullable=False)
    count = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # book = relationship("UserModel", back_populates="book_user")
