import asyncio
from aiogram import Bot, Dispatcher, F
from core.handlers.basic import get_start, location, delete_user, change_location, get_weather
from core.middlewares.settings import settings
from core.db.database import async_main
from aiogram.types import ContentType
from aiogram.filters import Command


async def start():
    bot = Bot(token=settings.bot_config.bot_token)

    dp = Dispatcher()
    dp.message.register(get_start, Command(commands=['start', 'commands']))
    dp.message.register(delete_user, Command(commands='delete'))
    dp.message.register(change_location, Command(commands='change_location'))
    dp.message.register(get_weather, Command(commands='get_current_weather'))
    dp.message.register(location, F.content_type == ContentType.LOCATION)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def start_bot():
    await asyncio.gather(async_main(), start())


if __name__ == '__main__':
    asyncio.run(start_bot())