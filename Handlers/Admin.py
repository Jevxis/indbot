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


"""


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
            data['number'] = int(message.text)
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
    await bot.send_message(message.from_user.id, "Данные добавлены")
    await state.finish()


# Выход из состояний
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ок')"""


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
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


# так как у нас все по разным файлам, то нужно зарегестрировать хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(delete_item, commands='Удалить')
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
