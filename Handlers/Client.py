import aiogram.types
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from data_base import sqlite_db
from keyboards import client_kb
from keyboards import kb_client


class FSMAdmin(StatesGroup):
    photo = State()
    city = State()
    street = State()
    number = State()
    describe = State()
    location_x = State()
    location_y = State()


class FSMfind(StatesGroup):
    find = State()


async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Привет! Я бот, который собирает информацию о различной '
                                                     'инфраструктуре городов, вы можете просмотреть места, '
                                                     'которые есть, либо загрузить свое место', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему: \n@indicator11_bot ')


async def commands_help(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Для просмотра мест напишите /места\n'
                                                     'Для загрузки своего места напишите /загрузить\n'
                                                     'Для поиска определенного места напишите /поиск места',
                                                      reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему: \n@indicator11_bot ')


async def place_command(message: types.Message):
    await sqlite_db.sql_read(message)


async def start_find(message: types.Message):
    await message.reply(
        'Введите описание места, которое хотите найти (с заглавной буквы), чтобы выйти из поиска, напишите /отмена')
    await FSMfind.next()


async def find_place(message: types.Message, state: FSMContext):
    if message.text != '/отмена':
        await sqlite_db.sql_search_city(message)
        await sqlite_db.sql_search_street(message)
        await sqlite_db.sql_search_describe(message)
    else:
        await message.reply('Вы вышли из поиска')
        await state.finish()


async def cm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply('Загрузите фото места')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Введите город')


async def load_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text.lower().capitalize()
    await FSMAdmin.next()
    await message.reply('Введите улицу')


async def load_street(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['street'] = message.text.lower().capitalize()
    await FSMAdmin.next()
    await message.reply('Введите номер дома')


async def load_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = int(message.text)
    await FSMAdmin.next()
    await message.reply('Введите описание данного места')


async def load_describe(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['describe'] = message.text.lower().capitalize()
    await FSMAdmin.next()
    await bot.send_message(message.from_user.id,
                           "Поделитесь геопозицией или введите координаты вручную\nнапример: xx.xxxxx, yy.yyyyy",
                           reply_markup=client_kb.kb_client1)


async def handle_location(message: types.Message, state: FSMContext):
    if isinstance(message.location, aiogram.types.Location):
        lat = message.location.latitude
        lon = message.location.longitude
        async with state.proxy() as data:
            data['location_x'] = lat
        await FSMAdmin.next()
        async with state.proxy() as data:
            data['location_y'] = lon
        await sqlite_db.sql_add_command(state)
        await bot.send_message(message.from_user.id, "Данные добавлены, для просмотра мест напишите /места",
                               reply_markup=client_kb.kb_client)
        await state.finish()
    else:
        lat, lon = message.text.split(', ')
        async with state.proxy() as data:
            data['location_x'] = lat
        await FSMAdmin.next()
        async with state.proxy() as data:
            data['location_y'] = lon
        await sqlite_db.sql_add_command(state)
        await bot.send_message(message.from_user.id, "Данные добавлены, для просмотра мест напишите /места",
                               reply_markup=client_kb.kb_client)
        await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSMfind.find:
        await state.finish()
    await state.finish()
    await message.reply('Ок')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start'])
    dp.register_message_handler(commands_help, commands=['help'])
    dp.register_message_handler(place_command, commands=['Места'])
    dp.register_message_handler(start_find, commands=['Поиск'])
    dp.register_message_handler(find_place, state=FSMfind.find)
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_city, state=FSMAdmin.city)
    dp.register_message_handler(load_street, state=FSMAdmin.street)
    dp.register_message_handler(load_number, state=FSMAdmin.number)
    dp.register_message_handler(load_describe, state=FSMAdmin.describe)
    dp.register_message_handler(handle_location,content_types=['location', 'text'], state=FSMAdmin.location_x)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
