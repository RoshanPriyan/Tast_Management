from fastapi import Depends, status
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from utils import CustomException, success_response, verify_token
from database import get_db
from book.schemas import BookSchema
from book.models import BookModel
from book.book_utils import check_admin_user
import traceback


async def update_book_api(
        book_id: int,
        data: BookSchema,
        session: AsyncSession = Depends(get_db),
        token: int = Depends(verify_token)
):
    try:
        await check_admin_user(token, session)

        already_exist = select(BookModel).where(BookModel.id == book_id)
        already_exist_exe = await session.execute(already_exist)
        check_book = already_exist_exe.scalars().one_or_none()

        if not check_book:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book id not found",
            )

        update_stmt = (
            update(BookModel)
            .where(BookModel.id == book_id)
            .values(
                title=data.title,
                description=data.description,
                author=data.author,
                count=data.count
        )
        )
        await session.execute(update_stmt)
        await session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            detail="Book details updated successfully"
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )