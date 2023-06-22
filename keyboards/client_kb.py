from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Места')
b2 = KeyboardButton('Отправить где я', request_location=True)
b3 = KeyboardButton('/Загрузить')
b4 = KeyboardButton('/Поиск места')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.insert(b1).add(b3).add(b4)
kb_client1 = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
kb_client1.add(b2)
