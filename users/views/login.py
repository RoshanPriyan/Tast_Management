from fastapi import status, Depends, BackgroundTasks
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from ..models import UserModel, UserAuthInfoModel
from ..schemas import LoginSchema
from global_utils import success_response, CustomException, generate_token
from database import get_db
import traceback
from tasks import confirm_email_status


async def user_login_api(
        data: LoginSchema,
        background: BackgroundTasks,
        session: AsyncSession = Depends(get_db)
):
    try:
        existing_user_check = select(UserModel).where(UserModel.username == data.username)
        existing_user_exe = await session.execute(existing_user_check)
        existing_user = existing_user_exe.scalars().first()
        
        if not existing_user or not existing_user.verify_password(data.password):
                raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or password"
            )

        if existing_user.status == 0:
            background.add_task(confirm_email_status, existing_user.username, existing_user.email)
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not active"
            )

        user_detail = {"user_id": existing_user.id}
        token = generate_token(user_detail)

        auth_info_query = select(UserAuthInfoModel).where(UserAuthInfoModel.user_id == existing_user.id)
        auth_info_result = await session.execute(auth_info_query)
        auth_info_entry = auth_info_result.scalars().one_or_none()

        if not auth_info_entry:
            add_token_user = UserAuthInfoModel(
                 user_id=existing_user.id,
                 token=token
            )
            session.add(add_token_user)
            await session.flush()
            await session.refresh(add_token_user)
        else:
            refresh_token = (
                 update(UserAuthInfoModel)
                 .where(UserAuthInfoModel.user_id == existing_user.id)
                 .values(token=token)
                 )
            await session.execute(refresh_token)

        await session.commit()

        user_data = {
             "username": existing_user.username,
             "email": existing_user.email,
             "role": existing_user.role,
             "token": token
        }

        return success_response(
            status_code=status.HTTP_200_OK,
            detail="User login successfully",
            data=user_data
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}Internal Server Error",
            error=str(e),
            trace_back=traceback.format_exc()
        )
