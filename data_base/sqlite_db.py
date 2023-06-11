import sqlite3 as sq
from create_bot import dp, bot




def sql_start():  # функция, которой создается база данных
    global base, cur
    base = sq.connect("pizza_cool.db")
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(photo TEXT, city TEXT, street TEXT, number TEXT, describe TEXT, location_x TEXT, location_y TEXT)')
    base.commit()  # сохранение этих изменений

    # запись изменеий в базу данных


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'Город: {ret[1]}\nУлица: {ret[2], ret[3]}\nОписание: {ret[4]}\nКоординаты: {ret[-2]}, {ret[-1]}')


async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def sql_delete_command(data):
    cur.execute("DELETE FROM menu WHERE city == ?", (data,))
    base.commit()
