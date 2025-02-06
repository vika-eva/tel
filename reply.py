from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_weather_by_city():
    get_weather_btn = KeyboardButton(text="Get Weather")
    get_user_id_btn = KeyboardButton(text="Get My Id")
    get_bot_info_btn = KeyboardButton(text="Get Bot Info")
    get_bot_info_btn_c = KeyboardButton(text="Get current exchange rate")
    exit_btn = KeyboardButton(text="Exit")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [get_weather_btn, get_user_id_btn, get_bot_info_btn],
            [get_bot_info_btn_c],
            [exit_btn]
        ]
    )
    return keyboard