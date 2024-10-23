from aiogram import Bot
from aiogram.types import Message
from core.keyboards.get_location_keyboard import get_location
from core.db.main_db import DBOperations
import json


commands = """
/start - start
/commands - commands
/delete - delete your account
/get_current_weather - send you current weather in your location
/change_location - change your location
"""


async def get_start(message: Message, bot: Bot):
    user_exists = await DBOperations.check_user_exists(message.from_user.id)

    if user_exists:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'commands:\n{commands}'
        )

    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='send your geo',
            reply_markup=get_location
        )


async def location(message: Message, bot: Bot):
    user_exists = await DBOperations.check_user_exists(message.from_user.id)

    if user_exists:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'Your account already exist'
        )

    else:
        try:
            user_id = message.from_user.id
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            username = message.from_user.username

            lat = message.location.latitude
            lon = message.location.longitude

            await DBOperations.create_user(
                user_id = user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                lat=lat,
                lon=lon
            )

            await bot.send_message(
                chat_id=message.from_user.id,
                text=f'commands:\n{commands}'
            )

        except Exception as error:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f'{error}'
            )


async def delete_user(message: Message, bot: Bot):
    user_exists = await DBOperations.check_user_exists(message.from_user.id)

    if user_exists:
        await DBOperations.delete_account(message.from_user.id)

        if await DBOperations.check_user_exists(message.from_user.id):
            text=f"Your account wasn't deleted"

        else:
            text=f"Your account was deleted"

        await bot.send_message(
            chat_id=message.from_user.id,
            text=text
        )


async def change_location(message: Message, bot: Bot):
    user_exists = await DBOperations.check_user_exists(message.from_user.id)

    if user_exists:
        await DBOperations.delete_account(message.from_user.id)

        user_exists = await DBOperations.check_user_exists(message.from_user.id)

        if user_exists:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"Something went wrong, try again"
            )

        else:
            await get_start(message, bot)


async def get_weather(message: Message, bot: Bot):
    user_exists = await DBOperations.check_user_exists(message.from_user.id)

    if user_exists:
        json_data = await DBOperations.get_weather(message.from_user.id)
        weather_data = json.loads(json_data)['data'][0]

        description = (
            f"DATA:\n"
            f"City: {weather_data['city_name']}\n"
            f"Air Quality Index: {weather_data['aqi']}/500\n"
            f"Clouds coverage: {weather_data['clouds']}%\n"
            f"Date-time: {weather_data['datetime']}\n"
            f"Dew point: {weather_data['dewpt']}°C\n"
            f"Direct normal solar irradiance: {weather_data['dni']}W/m^2\n"
            f"Diffuse horizontal solar irradiance: {weather_data['dhi']}W/m^2\n"
            f"Solar elevation angle: {weather_data['elev_angle']}W/m^2\n"
            f"Global horizontal solar irradiance: {weather_data['ghi']}W/m^2\n"
            f"Wind gust speed: {weather_data['gust']}m/s\n"
            f"Latitude: {weather_data['lat']}\n"
            f"Longitude: {weather_data['lon']}\n"
            f"Last observation time: {weather_data['ob_time']}\n"
            f"Part of the day: {weather_data['pod']}(d = day / n = night)\n"
            f"Liquid equivalent precipitation rate: {weather_data['precip']}mm/hr\n"
            f"Pressure: {weather_data['pres']}mb\n"
            f"Relative humidity: {weather_data['rh']}%\n"
            f"Sea level pressure: {weather_data['slp']}mb\n"
            f"Snowfall: {weather_data['snow']}mm/hr\n"
            f"Estimated Solar Radiation: {weather_data['solar_rad']}W/m^2\n"
            f"Sunrise time UTC: {weather_data['sunrise']}(HH:MM)\n"
            f"Sunset time UTC: {weather_data['sunset']}(HH:MM)\n"
            f"Temperature: {weather_data['temp']}°C\n"
            f"'Feels Like' temperature: {weather_data['app_temp']}°C\n"
            f"Timezone: {weather_data['timezone']}\n"
            f"UV Index: {weather_data['uv']}(0-11+)\n"
            f"Visibility: {weather_data['vis']}KM\n"
            f"Weather: {weather_data['weather']['description']}\n"
            f"Verbal wind direction: {weather_data['wind_cdir_full']}\n"
            f"Wind direction: {weather_data['wind_dir']}°\n"
            f"Wind speed: {weather_data['wind_spd']}m/s\n"
        )


        await  bot.send_message(
            chat_id=message.from_user.id,
            text=description
        )
