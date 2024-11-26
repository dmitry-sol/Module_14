import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

from config import *
from keyboards import *
from crud_functions import *
import texts

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())
activity_data = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9}


class UserState(StatesGroup):
    sex = State()
    age = State()
    height = State()
    weight = State()
    daily_activity = State()


@dp.message_handler(commands=['start'])
async def start(message):
    with open('files/start.gif', 'rb') as gif:
        await message.answer_video(gif)
    await message.answer(f'Добро пожаловать, {message.from_user.username}! '
                         + texts.start, reply_markup=kb_1)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    db_products = get_all_products()
    for i in range(4):
        with open(f'files/images {i + 1}.jpg', 'rb') as img:
            await message.answer_photo(img,
                                       f'Название: {db_products[i][1]} | Описание: {db_products[i][2]} | Цена: {db_products[i][3]}')
    await message.answer(texts.product_choice, reply_markup=inline_kb_2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(texts.confirm_message)
    await call.answer()


@dp.message_handler(text='Информация')
async def info(message):
    with open('files/images 0.jpg', 'rb') as img:
        await message.answer_photo(img, texts.info)


@dp.message_handler(text='Рассчитать')
async def calculate(message):
    await message.answer(texts.calculate, reply_markup=inline_kb_1)


@dp.callback_query_handler(text='calories')
async def set_sex(call):
    await call.message.answer(texts.set_sex, reply_markup=kb_2)
    await UserState.sex.set()
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def formula_info(call):
    await call.message.answer(texts.formula)
    await call.answer()


@dp.message_handler(state=UserState.sex)
async def set_age(message, state):
    await state.update_data(sex=message.text)
    await message.answer(texts.set_age)
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_height(message, state):
    await state.update_data(age=message.text)
    await message.answer(texts.set_height)
    await UserState.height.set()


@dp.message_handler(state=UserState.height)
async def set_weight(message, state):
    await state.update_data(height=message.text)
    await message.answer(texts.set_weight)
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_daily_activity(message, state):
    await state.update_data(weight=message.text)
    await message.answer(texts.set_daily_activity)
    await UserState.daily_activity.set()


@dp.message_handler(state=UserState.daily_activity)
async def send_calories(message, state):
    await state.update_data(daily_activity=message.text)
    data = await state.get_data()
    sex_index = 5 if data['sex'] == 'м' else -151
    calories = round((10 * int(data['weight']) + 6.25 * int(data['height']) - 5 * int(data['age'])
                      + sex_index) * activity_data[int(data['daily_activity'])])
    await message.answer(f'Ваша норма калорий: {calories}', reply_markup=kb_1)
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer(texts.any_text)


if __name__ == '__main__':

    initiate_db()

    products = [
        ('Vitamin C', 'От простуды', 419.99),
        ('Vitamin D3', 'Для сосудов', 560.00),
        ('Vitamin A', 'Для зрения', 720.99),
        ('Vitamin E', 'Для сердца', 289.50)
    ]

    for i in range(len(products)):
        add_product(products[i][0], products[i][1], products[i][2])

    executor.start_polling(dp, skip_updates=True)