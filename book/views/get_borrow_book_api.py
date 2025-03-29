from fastapi import status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from database import get_db
from global_utils import CustomException, success_response, verify_token
from book.models import BookModel, BorrowBookModel
import traceback


async def get_borrow_book_api(
        session: AsyncSession = Depends(get_db),
        token_user: int = Depends(verify_token)
):
    try:
        get_borrow_book = (
            select(
                BookModel.title,
                BookModel.description,
                BookModel.author,
                BorrowBookModel.status,
                BorrowBookModel.borrow_date,
                BorrowBookModel.return_date
            )
            .join(BookModel, BookModel.id == BorrowBookModel.book_id)
            .where(BorrowBookModel.user_id == token_user))
        get_borrow_book_exe = await session.execute(get_borrow_book)
        get_borrow_book = get_borrow_book_exe.mappings().all()

        for index, data in enumerate(get_borrow_book):
            custom_dict = dict(data)
            borrow_date = custom_dict.pop("borrow_date").strftime("%y-%m-%d %H:%M:%S")
            return_date = custom_dict.get("return_date")
            custom_dict["borrow_date"] = borrow_date
            custom_dict["return_date"] = return_date.strftime("%y-%m-%d %H:%M:%S") if return_date else None
            get_borrow_book[index] = custom_dict

        return success_response(
            status_code=status.HTTP_200_OK,
            detail=f"Books retrieved successfully",
            data=get_borrow_book
        )
    except SQLAlchemyError as e:
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
