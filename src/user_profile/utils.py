import random
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from auth.models import users, tokens, employees
from database import get_async_session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN


async def select_token_by_access_token_from_db(access_token:  str,
                            session: AsyncSession = Depends(get_async_session)):

    query_token = select(tokens).where(tokens.c.access_token == access_token)
    result = await session.execute(query_token)
    get_token = result.first()
    return get_token


async def get_user_by_token(user_id: int, access_token:  str,
                            session: AsyncSession = Depends(get_async_session)):
    selected_token = await select_token_by_access_token_from_db(access_token, session)

    query_employee = select(employees)
    result = await session.execute(query_employee)
    get_employee = result.fetchall()

    if selected_token:
        if not any([selected_token[-1] == employee[1] for employee in get_employee]):
            stmt = insert(employees).values(id=get_employee[-1][0] + 1 if get_employee else 1,
                                            id_user=selected_token[-1],
                                            salary=random.randint(50000, 150000),
                                            next_grade_in=datetime.now() + timedelta(weeks=8))
            await session.execute(stmt)
            await session.commit()

    if selected_token:
        if selected_token[-1] == user_id:

            query_employee = select(employees).where(employees.c.id_user == selected_token[-1])
            result = await session.execute(query_employee)
            get_employee = result.first()

            if get_employee:
                query_user = select(users).where(users.c.id == selected_token[-1])
                result = await session.execute(query_user)
                get_user = result.fetchone()

                return {
                    "Salary": get_employee[-2],
                    "Next_grade_data": get_employee[-1],
                    "name": get_user[-1],
                    "surname": get_user[-2],
                    "email": get_user[1]
                }

        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="FORBIDDEN"
        )
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )