from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_add_user_if_not_exists, orm_get_user
from data_parse.driver import create_driver

from handlers.filters import personalCodeValid, profileNumberCheck

from data_parse.parse import get_profiles, get_stats

import handlers.keyboards as kb

router = Router()

class Reg(StatesGroup):
    personal_code = State()
    password = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Для парсинга данных нужен твой пароль и логин")

@router.message(Command('reg'))
async def auth(message: Message, state: FSMContext, session: AsyncSession):
    try:
        user_id = int(message.from_user.id)
        found_user = await orm_get_user(session, user_id)
        if found_user.user_id:
            print(f"Получили пользователя {found_user}")
            await message.answer("Ваши данные уже есть в системе, не хотите сразу зайти по уже известным данным?", reply_markup=kb.choice, one_time_keyboard=True)
    except Exception as e:
        print(e)

@router.message(F.text == "Отказаться")
async def register(message: Message, state: FSMContext):
    await state.set_state(Reg.personal_code)
    await message.answer('Введите свой персональный код', reply_markup=ReplyKeyboardRemove())

@router.message(Reg.personal_code)
async def reg_two(message: Message, state: FSMContext):
    if personalCodeValid(message.text):
        await state.update_data(code=message.text)
        await state.set_state(Reg.password)
        await message.answer('Введите свой пароль')
    else:
        await message.answer("Пожалуйста введите персональный код в правильном формате:\n Пример: 123456-78910")

@router.message(Reg.password)
async def two_three(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(password=message.text)
    data = await state.get_data()

    try:
        user_id = int(message.from_user.id)
        await orm_add_user_if_not_exists(session, user_id, data)
        await message.answer(f'Спасибо, мы получили ваши данные.\n'
                             f'Персональный код: {data["code"]}\n'
                             f'Пароль: <tg-spoiler>{data["password"]}</tg-spoiler>\n'
                             f'Готовы ли вы войти?', reply_markup=kb.auth, parse_mode='HTML', one_time_keyboard=True)
    except Exception as e:
        await message.answer(f"Ошибка: \n"
                             f"{str(e)}")

    await state.clear()

@router.message(F.text.in_(["Войти", "Продолжить"]))
async def login(message: Message, state: FSMContext, session: AsyncSession):
    user_id = int(message.from_user.id)
    user = await orm_get_user(session, user_id)

    code = user.code
    password = user.password

    if code and password:
        await message.answer("Подождите немного, производится запрос", reply_markup=ReplyKeyboardRemove())
        driver = create_driver()
        profiles = get_profiles(driver, code, password)

        response = "Удалось получить следующие профили:\n\n"
        for profile in profiles:
            response += (f"Профиль {profiles.index(profile)+1}\n"
                        f"👤 Имя: {profile['firstName']} {profile['lastName']}\n"
                        f"🏫 Школа: {profile['schoolName']}\n"
                        f"📚 Класс: {profile['className']}\n"
                        f"🎭 Роль: {profile['personTypeName']}\n\n")

        await message.answer(response, reply_markup=await kb.profiles(profiles))
        await state.update_data(profiles=profiles)
        await state.update_data(driver=driver)

@router.message(F.text.contains("Профиль"))
async def profile_fetch(message: Message, state: FSMContext):
    data = await state.get_data()
    profiles = data["profiles"]
    if profileNumberCheck(message.text, len(profiles)):
        profile_number = int(message.text.split(' ')[1])
        driver = data['driver']
        await message.answer(f"Получаем данные из {profile_number}-го профиля...")

        try:
            text = get_stats(driver, profiles[profile_number-1], 1)
            await message.answer(text)
        except Exception as e:
            await message.answer(str(e))
        finally:
            driver.close()
            driver.quit()
            await state.clear()

