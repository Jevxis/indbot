import sqlite3 as sq
from create_bot import dp, bot


def sql_start():  # функция, которой создается база данных
    global base, cur
    base = sq.connect("all_places.db")
    cur = base.cursor()
    if base:
        print('База данных подключена!')
    base.execute(
        'CREATE TABLE IF NOT EXISTS places(photo TEXT, city TEXT, street TEXT, number TEXT, describe TEXT, location_x '
        'TEXT, location_y TEXT)')
    base.commit()  # сохранение этих изменений

# запись изменений в базу данных


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO places VALUES (?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM places').fetchall():
        await bot.send_photo(message.from_user.id, ret[0],
                             f'Город: {ret[1]}\nУлица: {ret[2], ret[3]}\nОписание: {ret[4]}\nКоординаты: {ret[-2]}, {ret[-1]}')


async def sql_read2():
    return cur.execute('SELECT * FROM places').fetchall()


async def sql_search_city(message):
    search_query = message.text
    try:
        if cur.execute(f"SELECT * FROM places WHERE city LIKE ?", [f"%{search_query}%"]).fetchone()[1] == f'{search_query}':
            for ret in cur.execute(f"SELECT * FROM places WHERE city LIKE ?", [f"%{search_query}%"]).fetchall():
                await bot.send_photo(message.from_user.id, ret[0], f'Город: {ret[1]}\nУлица: {ret[2], ret[3]}\nОписание: {ret[4]}\nКоординаты: {ret[-2]}, {ret[-1]}')
        else:
            await message.reply("Такого места с данным описание не найдено")
    except:
        await message.reply("Города с таким названием не найдено")


async def sql_search_street(message):
    search_query = message.text
    try:
        if cur.execute(f"SELECT * FROM places WHERE street LIKE ?", [f"%{search_query}%"]).fetchone()[2] == f'{search_query}':
            for ret in cur.execute(f"SELECT * FROM places WHERE street LIKE ?", [f"%{search_query}%"]).fetchall():
                await bot.send_photo(message.from_user.id, ret[0], f'Город: {ret[1]}\nУлица: {ret[2], ret[3]}\nОписание: {ret[4]}\nКоординаты: {ret[-2]}, {ret[-1]}')
        else:
            await message.reply("Такого места с данным описание не найдено")
    except:
        await message.reply("Такой улицы не найдено")


async def sql_search_describe(message):
    search_query = message.text
    try:
        if cur.execute(f"SELECT * FROM places WHERE describe LIKE ?", [f"%{search_query}%"]).fetchone()[4] == f'{search_query}':
            for ret in cur.execute(f"SELECT * FROM places WHERE describe LIKE ?", [f"%{search_query}%"]).fetchall():
                await bot.send_photo(message.from_user.id, ret[0], f'Город: {ret[1]}\nУлица: {ret[2], ret[3]}\nОписание: {ret[4]}\nКоординаты: {ret[-2]}, {ret[-1]}')
        else:
            await message.reply("Такого места с данным описание не найдено")
    except:
        await message.reply("Такого места с данным описание не найдено")


async def sql_delete_command(data):
    cur.execute("DELETE FROM places WHERE location_y == ?", (data, ))
    base.commit()
