from fastapi import status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from utils import CustomException
from users.models import UserModel
from database import get_db

async def check_admin_user(
        user_id: int,
        session: AsyncSession
):
    check_user = select(UserModel.role).where(UserModel.id == user_id)
    check_user_exe = await session.execute(check_user)
    role = check_user_exe.scalars().first()

    if role != "ADMIN":
        raise CustomException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only 'ADMIN' can create book"
        )
    return True
