from fastapi import Depends, status, Query
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import TaskModel
from utils import success_response, CustomException
import traceback

async def list_tasks_api(
        session: AsyncSession = Depends(get_db),
        limit: int = Query(10, ge=1, le=100),
        page: int = Query(1, ge=1)
):
    try:
        count_query = select(TaskModel)
        count_res = await session.execute(count_query)
        total_records = len(count_res.scalars().all())

        offset = (page - 1) * limit

        task_query = (
            select(
                TaskModel.id,
                TaskModel.title,
                TaskModel.description,
                TaskModel.created_at,
                TaskModel.completed
            )
            .limit(limit)
            .offset(offset)
        )
        task_res = await session.execute(task_query)
        res = task_res.mappings().all()

        for index, data in enumerate(res):
            custom_dict = dict(data)
            custom_dict["created_at"] = custom_dict["created_at"].strftime("%Y-%m-%d %H:%M:%S")
            custom_dict["status"] = TaskModel.STATUS[0] if custom_dict.get("completed") else TaskModel.STATUS[1]
            res[index] = custom_dict

        total_pages = (total_records + limit - 1) // limit
        current_page = page
        previous_page = current_page - 1 if current_page > 1 else None
        next_page = current_page + 1 if current_page < total_pages else None

        if not res:
            return success_response(
                status_code=status.HTTP_200_OK,
                detail="Tasks not found",
                data=[],
                total_pages=total_pages,
                previous_page=previous_page,
                current_page=page,
                next_page=next_page,
                total=total_records,
                is_paginated=True,
            )
        return success_response(
            status_code=status.HTTP_200_OK,
            detail="Tasks retrieved successfully",
            data=res,
            total_pages=total_pages,
            previous_page=previous_page,
            current_page=page,
            next_page=next_page,
            total=total_records,
            is_paginated=True,
        )
    except CustomException as e:
        raise CustomException(
            status_code=e.status_code,
            detail=e.detail,
            error=str(e),
            trace_back=traceback.format_exc()
        )
