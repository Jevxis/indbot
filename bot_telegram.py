from aiogram.utils import executor
from create_bot import dp
from Handlers import Client, Admin, Other
from data_base import sqlite_db


async def on_startup(_):
    print('Бот готов к работе')
    sqlite_db.sql_start()


Client.register_handlers_client(dp)
Admin.register_handlers_admin(dp)
Other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
