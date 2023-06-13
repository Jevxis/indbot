import sqlite3 as sq
from create_bot import dp, bot


def sql_start(): 
    global base, cur
    base = sq.connect("all_places.db")
    cur = base.cursor()
    if base:
        print('База данных подключена!')
    base.execute(
        'CREATE TABLE IF NOT EXISTS places(photo TEXT, city TEXT, street TEXT, number TEXT, describe TEXT, location_x '
        'TEXT, location_y TEXT)')
    base.commit() 


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


async def sql_delete_command(data):
    cur.execute("DELETE FROM places WHERE location_y == ?", (data,))
    base.commit()
