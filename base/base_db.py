import sqlite3 as sq

def start_db():
    global base, cur
    base = sq.connect('../pride.db')
    cur = base.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS secret_users(\
            id INTEGER PRIMARY KEY AUTOINCREMENT,\
            telegram_id TEXT,\
            date TEXT,\
            room TEXT\
            amount TEXT\
            )'
    )
    base.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS asc(\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        platform TEXT,\
        login TEXT,\
        pass TEXT,\
        email TEXT,\
        email_pass TEXT,\
        photo_id TEXT,\
        user_id INT\
    )')
    cur.execute('CREATE TABLE IF NOT EXISTS user(\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        user_id INT,\
        user_name TEXT,\
        date TEXT,\
        state INT\
    )')
    cur.execute('CREATE TABLE IF NOT EXISTS senet_acs(\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        login TEXT,\
        email TEXT,\
        password TEXT,\
        name TEXT,\
        phone TEXT,\
        telegram_id INT\
    )')
    base.commit()


def get_user_data(tg_id: int)-> list: 
    user_data = cur.execute(
        f'SELECT * FROM secret_users WHERE telegram_id = \'{str(tg_id)}\''
    ).fetchone()
    if not user_data:
        return False
    else:
        return True


def append_user(tg_id: int):
    cur.execute(
        'INSERT INTO secret_users VALUES (?,?,?,?,?)',
        (None, tg_id, '0', '0', '0')
    )
    base.commit()


def check_user_in_prideDB(tg_id):
    user_data = cur.execute(
        f'SELECT * FROM senet_acs WHERE telegram_id = \'{str(tg_id)}\''
    ).fetchone()
    if user_data:
        return user_data[1]
    else:
        return False


def insert_new_user(tg_id):
    cur.execute(
        'INSERT INTO secret_users VALUES(?,?,?,?,?)',
        (None, tg_id, None, None, None)
    )
    base.commit()

def approve_reserv_db(tg_id, date, room, amount):
    cur.execute(
        f'UPDATE secret_users SET date = \'{date}\', room = \'{room}\', amount = \'{amount}\' WHERE telegram_id = \'{str(tg_id)}\''
    )
    base.commit()

def all():
    lis = [
        user for user in cur.execute(
            f'SELECT * FROM secret_users WHERE room != \'{None}\''
        ).fetchall()
    ]
    return lis


def secret_users():
    list_user = [
        user[1] for user in cur.execute(
            'SELECT * FROM secret_users'
        ).fetchall()
    ]
    return list_user


def all_tg_id():
    list1 = [
        id[1] for id in cur.execute(
            'SELECT * FROM secret_users'
        ).fetchall()
    ]
    return list1
