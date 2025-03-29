from fastapi import status, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from global_utils import success_response, CustomException, verify_token
from book.models import BookModel
import traceback

async def get_all_book_api(
        request: Request,
        session: AsyncSession = Depends(get_db),
        token_user: int = Depends(verify_token)
):
    try:
        books_stmt = select(BookModel.id, BookModel.title, BookModel.description, BookModel.author, BookModel.count)
        books_exe = await session.execute(books_stmt)
        books_res = books_exe.mappings().all()

        return success_response(
            status_code=status.HTTP_200_OK,
            detail="Books retrieved successfully",
            data=books_res
        )
    except SQLAlchemyError as e:
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
