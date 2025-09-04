from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import handlers.keyboards as kb
from handlers.middlewares import TestMIddleware

router = Router()

router.message.outer_middleware(TestMIddleware())

class Reg(StatesGroup):
    personal_code = State()
    password = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!", reply_markup=kb.main)

@router.message(Command('reg'))
async def get_personal_code(message: Message, state: FSMContext):
    await state.set_state(Reg.personal_code)
    await message.answer('Введите свой персональный код')

@router.message(Reg.personal_code)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.password)
    await message.answer('Введите свой пароль')

@router.message(Reg.password)
async def two_three(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f'Спасибо, регистрация завершена.\nИмя: {data["name"]}\nНомер: {data["number"]}')
    await state.clear()