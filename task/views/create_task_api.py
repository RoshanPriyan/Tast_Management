from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from ..models import TaskModel
from database import get_db
from ..schema import TaskSchema
from global_utils import success_response, CustomException, verify_token
import traceback


async def create_task_api(
        data: TaskSchema,
        session: AsyncSession = Depends(get_db),
        token_user: int = Depends(verify_token)
)->dict:
    try:
        add_task = insert(TaskModel).values(
            title=data.title,
            description=data.description,
            completed=data.completed,
            user_id=token_user
            )
        await session.execute(add_task)
        await session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            detail="task created successfully"
        )
    except CustomException as e:
        await session.rollback()
        raise CustomException(
        status_code=e.status_code,
        detail=e.detail,
        error=str(e),
        trace_back=traceback.format_exc()
        )
