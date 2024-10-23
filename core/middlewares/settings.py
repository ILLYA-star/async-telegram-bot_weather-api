import os
from dataclasses import dataclass


@dataclass
class BotConfig:
    bot_token: str


@dataclass
class APIConfig:
    https: str
    api: str


@dataclass
class DBConfig:
    dialect: str
    driver: str
    user: str
    password: str
    host: str
    port: str
    database: str


@dataclass
class Settings:
    bot_config: BotConfig
    api_config: APIConfig
    db_config: DBConfig


def get_settings():
    return Settings(
        bot_config=BotConfig(
            bot_token=os.getenv('TOKEN')
        ),
        api_config=APIConfig(
            https=os.getenv('HTTPS'),
            api=os.getenv('API')
        ),
        db_config=DBConfig(
            dialect=os.getenv('DIALECT'),
            driver=os.getenv('DRIVER'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            host=os.getenv('HOST'),
            port=os.getenv('PORT'),
            database=os.getenv('DATABASE')
        )
    )

settings = get_settings()
