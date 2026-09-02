import os
import sys
from dotenv import load_dotenv
import asyncio
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.types import Message
from asgiref.sync import sync_to_async
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiohttp
from mysite.tasks import check_all_price


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TgBot_WB.settings')
import django
django.setup()

from mysite.models import TgUser, Cryptocurrency, UserTracking

TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')
bot = Bot(token=TOKEN)

dp = Dispatcher()


class TrackForm(StatesGroup):
    cryptocurrency = State()
    waiting_for_target_price = State()

session: aiohttp.ClientSession | None = None

async def init_session():
    global session
    session = aiohttp.ClientSession()

async def close_session():
    if session:
        await session.close()

async def get_cryptocurrency(name: str) -> dict:
    url = (
        f'https://api.coingecko.com/api/v3/simple/price?'
        f'vs_currencies=usd&ids={name}&x_cg_demo_api_key={API_KEY}'
    )
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        print(f"Network error: {e}")
        return {}
    except asyncio.TimeoutError:
        print("Timeout while fetching crypto price")
        return {}


@sync_to_async
def create_tg_user(telegram_id, username):
    return TgUser.objects.get_or_create(telegram_id=telegram_id, username=username)

@sync_to_async
def create_cryptocurrency(name, coin_id, price):
    return Cryptocurrency.objects.get_or_create(coin_id=coin_id, defaults={'name': name, 'price': price})

@sync_to_async
def create_user_tracking(user,target_price, cryptocurrency):
    tracking, created = UserTracking.objects.get_or_create(user=user, cryptocurrency=cryptocurrency, defaults={'target_price': target_price})
    if not created and tracking.target_price != target_price:
        tracking.target_price = target_price
        tracking.save()
    return tracking

@sync_to_async
def get_cryptocurrency_by_id(cryptocurrency_id):
    try:
        return Cryptocurrency.objects.get(id=cryptocurrency_id)
    except Cryptocurrency.DoesNotExist:
        return None

@dp.message(Command('start'))
async def start_command(message: Message, state: FSMContext):
    check_all_price.delay()
    await create_tg_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Добро пожаловать {message.from_user.username}!\nОтправьте название криптовалюты, которую вы хотите отслеживать!")

@dp.message(TrackForm.waiting_for_target_price)
async def target_price_command(message: Message, state: FSMContext):
    try:
        target_price = float(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите число")
        return

    data = await state.get_data()
    user, _ = await create_tg_user(message.from_user.id, message.from_user.username)
    cryptocurrency_id = data.get('cryptocurrency_id')
    if not cryptocurrency_id:
        await message.answer("Что-то пошло не так. Попробуйте сначала.")
        await state.clear()
        return

    cryptocurrency = await get_cryptocurrency_by_id(cryptocurrency_id)
    if not cryptocurrency:
        await message.answer("Монета не найдена в базе. Начните сначала.\nОтправьте название криптовалюты, которую вы хотите отслеживать!")
        await state.clear()
        return

    await create_user_tracking(user,target_price,cryptocurrency)
    await message.answer(f"Началось отслеживание {cryptocurrency.name} до цены {target_price}$!")
    await state.clear()

@dp.message(F.text)
async def text_command(message: Message, state: FSMContext):
    name = message.text.lower().strip()
    data = await get_cryptocurrency(name)
    if not data or name not in data:
        await message.answer("Монета не найдена. Попробуйте: Bitcoin, Ethereum, Cardano!")
        return
    price = data[name]['usd']
    cryptocurrency, _ = await create_cryptocurrency(name,name,price)

    await state.update_data(cryptocurrency_id=cryptocurrency.id)

    await message.answer("Введите целевую цену (в USD):")
    await state.set_state(TrackForm.waiting_for_target_price)

async def main():
    await init_session()
    try:
        await dp.start_polling(bot)
    finally:
        await close_session()

if __name__ == '__main__':
    asyncio.run(main())
