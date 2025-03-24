from fastapi import status
from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base
import bcrypt


class UserModel(Base):
    __tablename__ = "users"

    ROLE = ["ADMIN", "USER"]

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(250), unique=True, nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    hash_password = Column(String(500), unique=True, nullable=False)
    created_date = Column(TIMESTAMP, server_default=func.current_timestamp())
    role = Column(String, nullable=False)

    auth_info = relationship("UserAuthInfoModel", back_populates="user", cascade="all, delete")
    task_user = relationship("TaskModel", back_populates="task")


    @property
    def password(self):
        raise AttributeError("Password is write-only!")

    @password.setter
    def password(self, plain_password):
        salt = bcrypt.gensalt()
        self.hash_password = bcrypt.hashpw(plain_password.encode(), salt).decode()
    
    def verify_password(self, plain_password):
        """ Check if the provided password matches the stored hash """
        return bcrypt.checkpw(plain_password.encode(), self.hash_password.encode())

    @staticmethod
    def validate_role(role):
        """ Validates if the role is either ADMIN or USER """
        from utils import CustomException
        if role.upper() not in UserModel.ROLE:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role! Allowed roles: 'ADMIN' or 'USER'"
            )
        return role.upper()     


class UserAuthInfoModel(Base):
    __tablename__ = "users_auth_info"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_date = Column(TIMESTAMP, server_default=func.current_timestamp())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(250), nullable=False)

    user = relationship("UserModel", back_populates="auth_info")
