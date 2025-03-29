from fastapi import Depends, status
from sqlalchemy import update, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from global_utils import success_response, CustomException, verify_token
from book.models import BookModel, BorrowBookModel
import traceback
import time


async def return_book_api(
        book_id: int,
        session: AsyncSession = Depends(get_db),
        token_user: int = Depends(verify_token)
):
    try:
        get_book_details = (
            select(BorrowBookModel)
            .where(BorrowBookModel.book_id == book_id, BorrowBookModel.user_id == token_user,
                   BorrowBookModel.status == BorrowBookModel.STATUS[0])
        )
        get_book_details_exe = await session.execute(get_book_details)
        book_detail = get_book_details_exe.scalars().one_or_none()

        get_book = select(BookModel).where(BookModel.id == book_id)
        get_book_exe = await session.execute(get_book)
        book_tab = get_book_exe.scalars().one_or_none()

        if not book_detail:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No borrowed book found for this user."
            )

        update_status = (
            update(BorrowBookModel)
            .where(BorrowBookModel.book_id == book_id, BorrowBookModel.user_id == token_user,
                   BorrowBookModel.status == BorrowBookModel.STATUS[0])
            .values(status=BorrowBookModel.STATUS[1],return_date=func.current_timestamp())
        )
        await session.execute(update_status)

        book_tab.available_count += 1

        if book_tab.available_count > book_tab.count:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot return the book again, count mismatch."
            )

        await session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            detail=f"Book '{book_tab.title}' return successfully"
        )

    except SQLAlchemyError as e:
        await session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )