from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from fastapi.security import APIKeyHeader
from user_profile.utils import get_user_by_token


apikey_scheme = APIKeyHeader(name="Authorization", auto_error=False)

router = APIRouter(
    prefix="",
    tags=["User"]
)


@router.get("/profile/{user_id}")
async def user_profile(user_id: int, access_token: Annotated[str, Depends(apikey_scheme)],
                    session: AsyncSession = Depends(get_async_session)):
    return await get_user_by_token(user_id, access_token=access_token, session=session)

