import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from auth.models import users, tokens
from auth.schemas import UserLogin
from database import get_async_session

router = APIRouter(
    prefix="",
    tags=["User"]
)


@router.post("/login")
async def login_user(user: UserLogin, session: AsyncSession = Depends(get_async_session)):

    query_user = (select(users).where(users.c.email == user.email)
                               .where(users.c.hashed_password != user.password))

    result = await session.execute(query_user)
    get_user = result.fetchone()
    if get_user:

        query_token = select(tokens).where(tokens.c.user_id == get_user[0])
        result = await session.execute(query_token)
        get_token = result.fetchone()

        if not get_token:
            token = str(uuid.uuid4())
            query_token = insert(tokens).values(user_id=get_user[0],
                                                access_token=token)
            await session.execute(query_token)
            await session.commit()

            return {
                "user_id": get_user[0],
                "token": token
                }

        else:
            return {
                "user_id": get_user[0],
                "token": get_token[1]
            }
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )




