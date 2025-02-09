import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, User, BotCommand
from aiohttp import ClientResponseError
from reply import get_weather_by_city
from utils import config_logger, COMMANDS
from weather import Weather
from currency import *
from news import *
from pict_nasa import *
from database import db

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
    await db.add_user(user.id, user.full_name, user.username)

    resp_text = f'Привіт 😍 {user.full_name}! Я бот, подивись що я можу'
    await bot.set_my_commands(COMMANDS + [BotCommand(command="cmd_for_you", description="Test")])
    await message.answer(text=resp_text, reply_markup=get_weather_by_city())

@dp.message(F.text == "бот інфо")
async def get_bot_info(message: Message):
    await message.answer(f"Я {await bot.get_my_name()} моє id={bot.id}. Допоможу тобі з погодою, курсом валют, покажу гарне фото від NASA та розсмішу анекдотом")

@dp.message(F.text == "id користувача")
async def get_bot_info(message: Message):
    await message.answer(f"Твоє ім'я {message.from_user.full_name} та id={message.from_user.id}")

@dp.message(F.text == "погода")
async def get_bot_info(message: Message, state: FSMContext):
    await state.set_state(BotStates.wait_city_name)
    await message.answer("яке місто? тилькі будь ласка на англ мові: ")

@dp.message(F.text == "бот")
async def get_bot_info(message: Message):
    await message.answer(f"Я {await bot.get_my_name()} моє id={bot.id}")

WAIT_FOR_CITY = False

@dp.message(F.text == "курс валют")
async def course_index(message: Message):
    text = format_exchange()
    await message.answer(text)

@dp.message(F.text == "новини")
async def get_bot_info(message: Message):
    await message.answer(f"https://tsn.ua/")

@dp.message(F.text == "анекдот")
async def send_joke(message: Message):
    joke = get_random_joke()
    await message.answer(f"😂 Ось твій анекдот:\n\n{joke}")

@dp.message(F.text == "фото дня")
async def send_nasa_photo(message: types.Message):
    title, image_url = get_nasa_photo()
    if image_url:
        await bot.send_photo(message.chat.id, image_url, caption=f"🌌 {title}")
    else:
        await message.answer(f"❌ шось не так пішло")

async def main():
    await db.connect()
    await bot.set_my_commands(COMMANDS)
    try:
        await dp.start_polling(bot)
    finally:
        await db.disconnect()
# async def main():
#         await bot.set_my_commands(COMMANDS)
#         await dp.start_polling(bot)


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
