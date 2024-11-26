from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Информация'),
            KeyboardButton(text='Рассчитать')
        ]
    ], resize_keyboard=True
)

button_1 = KeyboardButton(text='Купить')
kb_1.add(button_1)

inline_kb_1 = InlineKeyboardMarkup()
inline_button_2 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button_3 = InlineKeyboardButton(text='Формула расчёта', callback_data='formulas')
inline_kb_1.add(inline_button_2)
inline_kb_1.add(inline_button_3)

inline_kb_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying'),
         InlineKeyboardButton(text='Product2', callback_data='product_buying'),
         InlineKeyboardButton(text='Product3', callback_data='product_buying'),
         InlineKeyboardButton(text='Product4', callback_data='product_buying')],
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
