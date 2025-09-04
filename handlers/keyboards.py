from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
    [InlineKeyboardButton(text='Корзина', callback_data='cart'), InlineKeyboardButton(text='Контакты', callback_data='contacts')]
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Youtube", url="https://youtube.com")],
])

cars = ['Tesla', 'Mercedes', "BMW"]

async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        keyboard.add(InlineKeyboardButton(text=car, callback_data=f'{car}'))
    return keyboard.adjust(2).as_markup()

