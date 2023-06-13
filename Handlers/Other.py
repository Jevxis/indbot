import json
import string
from aiogram import types, Dispatcher


async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(" ")}.intersection(
            set(json.load(open('cenz.json')))) != set():  # фильтр слов
        await message.reply('еще раз и за это никогда ... \n РАЗБАНА...\n  не будет!')
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)

