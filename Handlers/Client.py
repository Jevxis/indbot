from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from data_base import sqlite_db


async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Привет! Я бот, который собирает информацию о различной инфраструктуре городов', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему: \n@indicator11_bot ')


async def place_command(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(place_command, commands=['Места'])
