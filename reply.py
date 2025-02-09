from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_weather_by_city():
    get_weather_btn = KeyboardButton(text="погода")
    get_user_id_btn = KeyboardButton(text="id користувача")
    get_bot_info_btn = KeyboardButton(text="бот інфо")
    get_bot_info_btn_c = KeyboardButton(text="курс валют")
    get_bot_info_btn_n = KeyboardButton(text="новини")
    get_bot_info_btn_g = KeyboardButton(text="анекдот")
    get_bot_info_btn_p = KeyboardButton(text="фото дня")
    #exit_btn = KeyboardButton(text="Exit")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [get_weather_btn, get_user_id_btn, get_bot_info_btn],
            [get_bot_info_btn_c, get_bot_info_btn_n, get_bot_info_btn_g],
            [get_bot_info_btn_p]
        ]
    )
    return keyboard