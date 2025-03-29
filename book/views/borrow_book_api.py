from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from book.models import BookModel, BorrowBookModel
from global_utils import success_response, CustomException, verify_token
import traceback


async def borrow_book_api(
        book_id: int,
        session: AsyncSession = Depends(get_db),
        token_user: int = Depends(verify_token)
):
    try:
        check_book = select(BookModel).where(BookModel.id == book_id).with_for_update()
        check_book_exe = await session.execute(check_book)
        book_exist = check_book_exe.scalars().one_or_none()

        if not book_exist:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        if book_exist.available_count <=0:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book copies not available"
            )

        already_borrow = (
            select(BorrowBookModel)
            .where(BorrowBookModel.book_id == book_id, BorrowBookModel.user_id == token_user,
                   BorrowBookModel.status == BorrowBookModel.STATUS[0])
        )
        check_borrow_exe = await session.execute(already_borrow)
        existing_borrow = check_borrow_exe.scalars().one_or_none()

        if existing_borrow:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already borrowed this book. Please return it first."
            )

        book_exist.available_count -= 1

        borrow_book = BorrowBookModel(
            user_id=token_user,
            book_id=book_id,
            status=BorrowBookModel.STATUS[0]
        )
        session.add(borrow_book)
        await session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            detail=f"Book '{book_exist.title}' borrowed successfully"
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
