from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb, client_kb

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    city = State()
    street = State()
    number = State()
    describe = State()
    location_x = State()
    location_y = State()


# провеерка на доступ к админке
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Доступ к админке', reply_markup=admin_kb.button_case_admin)
    await message.delete()


# начало диалога загрузки нового пункта меню
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузите фото места')


# ловим первый ответ и пишем в словарь
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введите город')


# Ловим второй ответ
async def load_city(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['city'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите улицу')


# Ловим третий ответ
async def load_street(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['street'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите номер дома')

#
async def load_number(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = int(message.text)
        await FSMAdmin.next()
        await message.reply('Введите описание данного места')


async def load_describe(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['describe'] = message.text
        await FSMAdmin.next()
        await bot.send_message(message.from_user.id, "поделитесь геопозицией", reply_markup=client_kb.kb_client1)


async def handle_location(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    async with state.proxy() as data:
        data['location_x'] = lat
    await FSMAdmin.next()
    async with state.proxy() as data:
        data['location_y'] = lon
    await sqlite_db.sql_add_command(state)
    await state.finish()


# Выход из состояний
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


# так как у нас все по разным файлам, то нужно зарегестрировать хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_city, state=FSMAdmin.city)
    dp.register_message_handler(load_street, state=FSMAdmin.street)
    dp.register_message_handler(load_number, state=FSMAdmin.number)
    dp.register_message_handler(load_describe, state=FSMAdmin.describe)
    dp.register_message_handler(handle_location, content_types=['location'], state=FSMAdmin.location_x)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
