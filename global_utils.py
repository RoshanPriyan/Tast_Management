import jwt
import time
import uuid
from users.models import UserAuthInfoModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends, status
from database import get_db


def success_response(
        status_code, detail, data=None, previous_page=None, current_page=None, next_page=None, total=None,
        total_pages=None, is_paginated:bool = None
):
    response = {
        "status_code": status_code,
        "detail": detail
    }
    if data:
        response["data"] = data

    if is_paginated:
        response.update(
            {
                "previous_page": previous_page,
                "current_page": current_page,
                "next_page": next_page,
                "total_pages": total_pages,
                "total": total
        }
        )
    return response


class CustomException(Exception):
    def __init__(self, status_code, detail, error=None, trace_back=None):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail
        self.error = error
        self.trace_back = trace_back


SECRET_KEY = "AbC123!@#"
ALGORITHM = "HS256"

def generate_token(data: dict):
    data["exp"] = int(time.time()) + 3600
    data["jti"] = str(uuid.uuid4())
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


async def verify_token(
        request: Request,
        session: AsyncSession = Depends(get_db)
        ):
    token = request.headers.get("token")

    if not token:
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token missing in header"
        )
    
    get_token_query = select(UserAuthInfoModel).where(UserAuthInfoModel.token == token)
    get_token_exe = await session.execute(get_token_query)
    get_token = get_token_exe.scalars().one_or_none()

    if not get_token:
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
    return get_token.user_id
