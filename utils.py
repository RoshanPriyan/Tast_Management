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


# import jwt
# from datetime import datetime, timedelta

# # Secret key for encoding and decoding JWT
# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token valid for 1 hour

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
    
#     # Set expiration time
#     expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
    
#     # Generate token
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
# print(create_access_token({"user_id": 1}))


# def verify_access_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload  # Returns decoded data if valid
#     except jwt.ExpiredSignatureError:
#         return "Token has expired"
#     except jwt.InvalidTokenError:
#         return "Invalid token"






# def create_access_token(data: dict):
#     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# token = create_access_token({"user_id": 1})
# print(token)

# def verify_access_token(token: str):
#     try:
#         decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return decoded_token
#     except jwt.InvalidTokenError:
#         return "Invalid token"

# print(verify_access_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.ftVWQD9oDs-8zTWaaTAq9SYq21WJeq6Y_pz5NY6MII"))


# class UserToken:
#     SECRET_KEY = "@A1B2C3D4E5F6G7H8I9J!"
#     ALGORITHM = "HS256"

#     def generate_token(self, data: dict):
#         return jwt.encode(data, self.SECRET_KEY, algorithm=self.ALGORITHM)

#     def verify_token(self, token: str):
#         try:
#             decoded_token = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
#             return decoded_token
#         except jwt.InvalidTokenError:
#             return "Invalid token"


