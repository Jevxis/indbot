from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Места')
b2 = KeyboardButton('Отправить где я', request_location=True)
b3 = KeyboardButton('/Загрузить')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.insert(b1).add(b3)
kb_client1 = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
kb_client1.add(b2)
