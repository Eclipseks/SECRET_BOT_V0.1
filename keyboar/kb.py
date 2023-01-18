from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def subscribe_to_bot_kb(callb):
    kb = InlineKeyboardMarkup()
    but = InlineKeyboardButton(
        text='Хочу в SECRET ROOM🤫',
        callback_data=f'subscribe_{callb}'
    )
    kb.add(but)
    return kb


def admin_invite_kb(tg_id, username):
    kb = InlineKeyboardMarkup()
    but = InlineKeyboardButton(
        text='✅ Підтвердити',
        callback_data=f'approve_{tg_id}'
    )
    but1 = InlineKeyboardButton(
        text='❌ Відхилити',
        callback_data=f'cancel_{tg_id}'
    )
    if username:
        but2 = InlineKeyboardButton(
            text='📤 Повідомлення',
            url=f'https://t.me/{username}'
        )
    else:
        but2 = InlineKeyboardButton(
            text='❗️ Юзернейм відсутній.',
            callback_data='0'
        )
    kb.add(but).insert(but1).add(but2)
    return kb


def reserv_kb():
    kb = InlineKeyboardMarkup()
    but = InlineKeyboardButton(
        text='🔸Резерв',
        callback_data='make_res'
    )
    kb.add(but)
    return kb


def room_kb():
    kb = InlineKeyboardMarkup()
    but = InlineKeyboardButton(
        text='PREMIUM - 500 ₴',
        callback_data='premium'
    )
    but1 = InlineKeyboardButton(
        text='VIP - 700 ₴',
        callback_data='vip'
    )
    but2 = InlineKeyboardButton(
        text='SUPER VIP - 1000 ₴',
        callback_data='s_vip'
    )
    but3 = InlineKeyboardButton(
        text='STREAMING - 1000 ₴',
        callback_data='streaming'
    )
    but4 = InlineKeyboardButton(
        text='LUXE - 500 ₴',
        callback_data='luxe'
    )
    kb.add(but).add(but1).add(but2).add(but3).add(but4)
    return kb


def admin_kb(username):
    kb = InlineKeyboardMarkup()
    but = InlineKeyboardButton(
        text='✅ Підтвердити',
        callback_data='res_plus'
    )
    but1 = InlineKeyboardButton(
        text='❌ Відхилити',
        callback_data='res_minus'
    )
    but1_1 = InlineKeyboardButton(
        text='❌ SOLD OUT',
        callback_data='sold_out'
    )
    but1_2 = InlineKeyboardButton(
        text='❌ Нужно больше людей',
        callback_data='more_hum'
    ) 
    if username:
        but2 = InlineKeyboardButton(
            text='📤 Повідомлення',
            url=f'https://t.me/{username}'
        )
    else:
        but2 = InlineKeyboardButton(
            text='❗️ Юзернейм відсутній.',
            callback_data='0'
        )
    kb.add(but).insert(but1).add(but1_1).insert(but1_2).add(but2)
    return kb
