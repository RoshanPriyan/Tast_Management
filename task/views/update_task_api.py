from fastapi import Depends, status
from ..models import TaskModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from global_utils import CustomException, success_response
import traceback
from sqlalchemy.exc import SQLAlchemyError
import json
from redis_config import redis_client


async def update_task_api(
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

        update_query = update(TaskModel).values(completed=0).where(TaskModel.id == task_id)
        await session.execute(update_query)
        await session.commit()
        
        task_query = (
            select(
                TaskModel.id,
                TaskModel.title,
                TaskModel.description,
                TaskModel.created_at,
                TaskModel.completed
            )
        )
        task_res = await session.execute(task_query)
        res = task_res.mappings().all()

        for index, data in enumerate(res):
            custom_dict = dict(data)
            custom_dict["created_at"] = custom_dict["created_at"].strftime("%Y-%m-%d %H:%M:%S")
            custom_dict["status"] = TaskModel.STATUS[0] if custom_dict.get("completed") else TaskModel.STATUS[1]
            res[index] = custom_dict

        redis_client.set("task_list", json.dumps(res))

        return success_response(
            status_code=status.HTTP_200_OK,
            detail="Task updated successfully"
        )

    except SQLAlchemyError as e:
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
            error=str(e),
            trace_back=traceback.format_exc()
        )
