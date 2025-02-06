import asyncio
import json
import os
from datetime import datetime
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, User, BotCommand, CallbackQuery, InlineKeyboardMarkup
from aiohttp import ClientResponseError, request
from reply import get_weather_by_city
from utils import config_logger, COMMANDS
from weather import Weather


TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
URL_API_BANK=os.getenv('URL_API_BANK')
dp = Dispatcher()
logger = config_logger()

class BotStates(StatesGroup):
    wait_city_name = State()
    default = State()



@dp.message(CommandStart())
async def start_command(message: Message):
    logger.info(f'user send /start to bot'
                f'Message(id={message.message_id}, text={message.text}),'
                f'from={message.from_user.id}')
    user: User = message.from_user

    logger.info(f'user info: User(id={user.id}, '
                f'name={user.full_name}), '
                f'username={user.username},'
                f'photo={user.get_profile_photos()}')
    resp_text = f'Hello {user.full_name}! I am bot'
    await bot.set_my_commands(COMMANDS + [BotCommand(command="cmd_for_you", description="Test")])
    await message.answer(text=resp_text, reply_markup=get_weather_by_city())

@dp.message(F.text == "Get Bot Info")
async def get_bot_info(message: Message):
    await message.answer(f"I am {await bot.get_my_name()} with id={bot.id}")

@dp.message(F.text == "Get My Id")
async def get_bot_info(message: Message):
    await message.answer(f"You are {message.from_user.full_name} with id={message.from_user.id}")

@dp.message(F.text == "Get Weather")
async def get_bot_info(message: Message, state: FSMContext):
    await state.set_state(BotStates.wait_city_name)
    await message.answer("send city name: ")

@dp.message(F.text == "Get current exchange rate")
async def course_index(message:Message):
    await message.answer(f"send current exchange rate: {load_exchange()}")


@dp.message(F.text == "Get exchange rate")
async def get_bot_info(message: Message):
    await message.answer(f"I am {await bot.get_my_name()} with id={bot.id}")

WAIT_FOR_CITY = False

def load_exchange():
    return json.loads(requests.get(URL_API_BANK).text)



async def main():
        await bot.set_my_commands(COMMANDS)
        await dp.start_polling(bot)


@dp.message(BotStates.wait_city_name)
async def get_weather_for_city(message: Message, state: FSMContext):
    try:
        weather = await (Weather().get_current(message.text))
        await message.answer(weather.as_text())
    except ClientResponseError as e:
        await message.answer(f"error: {e.message}")
    finally:
        await state.clear()


@dp.message()
async def all_message_handler(message: Message):
    await message.answer(f"Message with text {message.text} is not supported")

if __name__ == '__main__':
    logger.info("Start Bot")
    asyncio.run(main())
