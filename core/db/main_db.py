from select import select
from sqlalchemy.future import select
from core.db.database import engine, Users
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from core.middlewares.settings import settings
import aiohttp


class DBOperations:

    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    @classmethod
    async def create_user(
            cls, user_id: int, first_name:str,
            last_name:str, username:str,
            lat: float, lon: float
    ) -> None:

        user_exists = await cls.check_user_exists(user_id)

        if not user_exists:
            async with cls.async_session() as session:
                user = Users(
                    user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    lat=lat,
                    lon=lon
                )
                session.add(user)
                await session.commit()


    @classmethod
    async def get_user(cls, user_id: int):
        async with cls.async_session() as session:

            query = select(Users).filter(Users.user_id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            return user


    @classmethod
    async def check_user_exists(cls, user_id: int) -> bool:
        user = await cls.get_user(user_id)
        return user is not None


    @classmethod
    async def delete_account(cls, user_id: int) -> None:
        async with cls.async_session() as session:
            user = await cls.get_user(user_id)

            if user:
                await session.delete(user)
                await session.commit()


    @classmethod
    async def get_lat(cls, user_id: int) -> float:
        async with cls.async_session() as session:

            query = select(Users.lat).filter(Users.user_id == user_id)
            result = await session.execute(query)
            lat = result.scalars().first()

            return lat


    @classmethod
    async def get_lon(cls, user_id: int) -> float:
        async with cls.async_session() as session:

            query = select(Users.lon).filter(Users.user_id == user_id)
            result = await session.execute(query)
            lon = result.scalars().first()

            return lon


    @classmethod
    async def get_weather(cls, user_id: int):
        lat = await cls.get_lat(user_id)
        lon = await cls.get_lon(user_id)

        api = settings.api_config.api
        https = settings.api_config.https

        url = f"{https}?lat={lat}&lon={lon}&key={api}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
