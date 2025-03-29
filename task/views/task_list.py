from fastapi import Depends, status
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import TaskModel
from global_utils import success_response, CustomException
import traceback
from redis_config import redis_client
import json


async def task_list_api(
        session: AsyncSession = Depends(get_db)
):
    try:
        task_list = "task_list"
        cached_data = redis_client.get(task_list)

        if cached_data:
            return success_response(
                status_code=status.HTTP_200_OK,
                detail="Tasks retrieved successfully",
                data=json.loads(cached_data)
        )

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

        redis_client.set(task_list, json.dumps(res))

        return success_response(
            status_code=status.HTTP_200_OK,
            detail="Tasks retrieved successfully",
            data=res
        )
    except CustomException as e:
        raise CustomException(
            status_code=e.status_code,
            detail=e.detail,
            error=str(e),
            trace_back=traceback.format_exc()
        )
