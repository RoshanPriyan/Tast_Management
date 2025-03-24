from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    STATUS = ["COMPLETED", "PENDING"]

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    task = relationship("UserModel", back_populates="task_user")
