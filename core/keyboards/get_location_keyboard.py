from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


get_location = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Send Geo',
                request_location=True
            )
        ]
    ],
    resize_keyboard=True
)
