from datetime import datetime
from sqlalchemy import insert, select
from httpx import AsyncClient
from auth.models import tokens, users
from conftest import async_session_maker


""" TESTING DATABASE"""


async def test_add_user():
    date = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')

    async with async_session_maker() as session:
        stmt = insert(users).values(
            id=1,
            email="forjober@yandex.ru",
            hashed_password="$argon2id$v=19$m=65536,t=3,p=4$9fTYwfEtSP1YJpK4MFFl6w$Kib6fEzDAbbdc33UqxIpvy1b5BaYooJJs4FXRXNOhd0",
            registered_at=date,
            is_active=True,
            is_superuser=False,
            is_verified=False,
            surname="shunaev",
            name="nikita")
        await session.execute(stmt)
        await session.commit()

        query = select(users)
        result = await session.execute(query)
        assert result.all() == [(
            1, "forjober@yandex.ru",
        "$argon2id$v=19$m=65536,t=3,p=4$9fTYwfEtSP1YJpK4MFFl6w$Kib6fEzDAbbdc33UqxIpvy1b5BaYooJJs4FXRXNOhd0",
        date,
        True,
        False,
        False,
        "shunaev",
        "nikita")]


async def test_add_token():
    async with async_session_maker() as session:
        stmt = insert(tokens).values(
            id=1,
            access_token="$argon2id$v=19$m=65536,t=3,p=4$qgf2eDVNYhYnVjo4hLd7JQ$PzQI81AalpVGs5BVVjAe/xyuhyUmii5yuzuOS2mZdRA",
            user_id=1)
        await session.execute(stmt)
        await session.commit()

        query = select(tokens)
        result = await session.execute(query)
        assert result.all() == [
            (1,
             "$argon2id$v=19$m=65536,t=3,p=4$qgf2eDVNYhYnVjo4hLd7JQ$PzQI81AalpVGs5BVVjAe/xyuhyUmii5yuzuOS2mZdRA",
            1)]


""" TESTING API"""


async def test_api_login_success(ac: AsyncClient):
    response = await ac.post("/login", json={
        "email": "forjober@yandex.ru",
        "password": "$argon2id$v=19$m=65536,t=3,p=4$9fTYwfEtSP1YJpk4MFFl6w$Kib6fEzDAbbdc33UqxIpvy1b5BaYooJJs4FXRXNOhd0",
    })

    assert response.status_code == 200


async def test_api_login_failed(ac: AsyncClient):
    response = await ac.post("/login", json={
        "email": "jober@yandex.ru",
        "password": "$argon2id$v=19$m=65536,t=3,p=4$9fTYwfEtSP1YJpk4MFFl6w$Kib6fEzDAbbdc33UqxIpvy1b5BaYooJJs4FXRXNOhd0",
    })

    assert response.status_code == 401


async def test_api_profile_success(ac: AsyncClient):
    response = await ac.get("/profile/1", headers={
        "Content-Type": 'application/json',
        "Authorization":
            "$argon2id$v=19$m=65536,t=3,p=4$qgf2eDVNYhYnVjo4hLd7JQ$PzQI81AalpVGs5BVVjAe/xyuhyUmii5yuzuOS2mZdRA",
    })

    assert response.status_code == 200


async def test_api_profile_failed(ac: AsyncClient):
    response = await ac.get("/profile/2", headers={
        "Content-Type": 'application/json',
        "Authorization":
            "$argon2id$v=19$m=65536,t=3,p=4$qgf2eDVNYhYnVjo4hLd7JQ$PzQI81AalpVGs5BVVjAe/xyuhyUmii5yuzuOS2mZdRA",
    })

    assert response.status_code == 403
