from fastapi import status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from global_utils import success_response, CustomException, verify_token
from database import get_db
from book.schemas import BookSchema
from book.models import BookModel
from users.models import UserModel
import traceback


async def create_book_api(
        data: BookSchema,
        session: AsyncSession = Depends(get_db),
        token_user: int = Depends(verify_token)
):
    try:
        check_user = select(UserModel.role).where(UserModel.id == token_user)
        check_user_exe = await session.execute(check_user)
        role = check_user_exe.scalars().first()

        if role != "ADMIN":
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only 'ADMIN' can create book"
            )
        check_book_exist = select(BookModel).where(BookModel.title == data.title)
        check_book_exist_exe = await session.execute(check_book_exist)
        book_exist = check_book_exist_exe.scalars().one_or_none()

        if book_exist:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book already exist"
            )

        add_book = BookModel(
            title=data.title,
            description=data.description,
            author=data.author,
            count=data.count,
            user_id=token_user,
            available_count=data.count
        )
        session.add(add_book)
        await session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            detail="Book created successfully"
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
