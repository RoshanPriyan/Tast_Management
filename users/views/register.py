from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from utils import CustomException, success_response
from ..models import UserModel
from ..schemas import UserSchema
from database import get_db
import traceback


async def user_register_api(
        data: UserSchema,
        session: AsyncSession = Depends(get_db)
):
    try:
        existing_user_check = select(UserModel).where(UserModel.username == data.username)
        existing_user_exe = await session.execute(existing_user_check)
        existing_user = existing_user_exe.scalars().one_or_none()

        if existing_user is not None:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exist"
            )
        role = UserModel.validate_role(data.role)

        add_user_detail = UserModel(
            username=data.username,
            password=data.password,
            email=data.email,
            role=role
        )
        session.add(add_user_detail)
        await session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            detail="User register successfully"
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
