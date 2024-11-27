import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

from config import *
from crud_functions import *
import texts
from keyboards import *

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


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(commands=['start'])
async def start(message):
    with open('files/start.gif', 'rb') as gif:
        await message.answer_video(gif)
    await message.answer(f'Добро пожаловать, {message.from_user.username}! '
                         + texts.start, reply_markup=kb_1)


@dp.message_handler(text='Информация')
async def info(message):
    with open('files/images 0.jpg', 'rb') as img:
        await message.answer_photo(img, texts.info)


@dp.message_handler(text=['Регистрация'])
async def sing_up(message):
    await message.answer(texts.set_username)
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    if is_included(message.text):
        await message.answer(texts.name_is_busy)
        await RegistrationState.username.set()
    else:
        await message.answer(texts.set_email)
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer(texts.set_age_)
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer(f'Пользователь {data["username"]} успешно зарегистрирован', reply_markup=kb_1)
    await state.finish()



@dp.message_handler(text='Купить')
async def get_buying_list(message):
    db_products = get_all_products()

    def get_image_path(product_name):
        image_path = f'files/{product_name}.jpg'
        return image_path if os.path.exists(image_path) else 'files/no_image.jpg'

    for product in db_products:
        image_path = get_image_path(product[1])
        with open(image_path, 'rb') as img:
            await message.answer_photo(
                img,
                f'Название: {product[1]} | '
                f'Описание: {product[2]} | '
                f'Цена: {product[3]}'
            )
    await message.answer(texts.product_choice, reply_markup=inline_kb_2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(texts.confirm_message)
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def calculate(message):
    await message.answer(texts.calculate, reply_markup=inline_kb_1)


@dp.callback_query_handler(text='formulas')
async def formula_info(call):
    await call.message.answer(texts.formula, reply_markup=inline_kb_1)
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_sex(call):
    await call.message.answer(texts.set_sex, reply_markup=kb_2)
    await UserState.sex.set()
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
    for product in products:
        add_product(product[0], product[1], product[2])

    users = [
        ('Alfa', 'a@gmail.com', 11),
        ('Bravo', 'b@gmail.com', 22),
        ('Charly', 'c@gmail.com', 33),
        ('Delta', 'd@gmail.com', 44)
    ]
    for user in users:
        if is_included(user[0]) is False:
            add_user(user[0], user[1], user[2])

    executor.start_polling(dp, skip_updates=True)
