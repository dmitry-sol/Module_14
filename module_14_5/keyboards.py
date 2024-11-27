from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import get_all_products

kb_1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Информация'),
            KeyboardButton(text='Рассчитать')
        ],
        [
            KeyboardButton(text='Регистрация'),
            KeyboardButton(text='Купить')
        ]
    ], resize_keyboard=True
)


inline_kb_1 = InlineKeyboardMarkup()
inline_button_2 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button_3 = InlineKeyboardButton(text='Формула расчёта', callback_data='formulas')
inline_kb_1.add(inline_button_2)
inline_kb_1.add(inline_button_3)

db_products = get_all_products()
if not db_products:
    inline_kb_2 = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Нет доступных товаров", callback_data='no_products')]
        ]
    )
else:
    inline_kb_2 = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'{product[1]}', callback_data='product_buying')
             for product in db_products[:len(db_products)]]
        ]
    )

kb_2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='м'),
            KeyboardButton(text='ж')
        ]
    ], resize_keyboard=True
)
