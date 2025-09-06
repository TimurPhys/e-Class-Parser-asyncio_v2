from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

auth = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Войти')]
], resize_keyboard=True)

choice = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Продолжить'), KeyboardButton(text='Отказаться')]
], resize_keyboard=True)


cars = ['Tesla', 'Mercedes', "BMW"]

async def profiles(profiles):
    keyboard = ReplyKeyboardBuilder()
    for i in range(1, len(profiles)+1):
        keyboard.add(KeyboardButton(text=f"Профиль {i}"))
    return keyboard.adjust(3).as_markup(resize_keyboard=True, one_time_keyboard=True)

