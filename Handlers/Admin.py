from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import bot
from data_base import sqlite_db
from keyboards import admin_kb

ID = None


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Доступ к админке', reply_markup=admin_kb.button_case_admin)
    await message.delete()


async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text="удалено", show_alert=True)


async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f"Город: {ret[1]}\nУлица: {ret[2], ret[3]}\nОписание:\
{ret[4]}\nКоординаты: {ret[-2]}, {ret[-1]}")
            await bot.send_message(message.from_user.id, text='Удалить место выше?',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(f"Удалить {ret[1]}\n{ret[2], ret[3]}",
                                                            callback_data=f'del {ret[-1]}')))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(delete_item, commands='Удалить')
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
