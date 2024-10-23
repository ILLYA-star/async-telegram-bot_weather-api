from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import BigInteger
from core.middlewares.settings import settings


dialect = settings.db_config.dialect
driver = settings.db_config.driver
user = settings.db_config.user
password = settings.db_config.password
host = settings.db_config.host
port = settings.db_config.port
database = settings.db_config.database

url = f"{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}"

engine = create_async_engine(url)


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str]
    lat: Mapped[float]
    lon: Mapped[float]

    last_name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]


async def async_main() -> None:

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

