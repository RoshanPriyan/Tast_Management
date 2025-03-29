from fastapi import Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import TaskModel
from sqlalchemy import select, delete
from database import get_db
from global_utils import CustomException, success_response
import traceback


async def delete_task_api(
        session: AsyncSession = Depends(get_db),
        task_id = int
):
    try:
        existing_task = select(TaskModel).where(TaskModel.id == task_id)
        existing_task_exe = await session.execute(existing_task)
        exist_task = existing_task_exe.scalars().first()

        if not exist_task:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task not found"
            )

        delete_query = delete(TaskModel).where(TaskModel.id == task_id)
        await session.execute(delete_query)
        await session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            detail="Task deleted successfully"
        )

    except SQLAlchemyError as e:
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
            error=str(e),
            trace_back=traceback.format_exc()
        )
