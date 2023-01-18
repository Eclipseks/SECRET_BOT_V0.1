import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile

from config import dp, bot, CHECK_GROUP, APPROVE_PHOTO
from keyboar.kb import subscribe_to_bot_kb, admin_invite_kb, reserv_kb, room_kb, admin_kb
from base.base_db import get_user_data, check_user_in_prideDB, insert_new_user, approve_reserv_db, all, secret_users, check_user_in_prideDB, all_tg_id
from func.card import get_photo_from_card
import caption.caption as cap


@dp.message_handler(commands='start')
async def start(message: types.Message, state=FSMContext):
    await bot.delete_message(
        message.chat.id,
        message.message_id
    )

    checker_pride = check_user_in_prideDB(
        message.from_user.id
    )
    if not checker_pride:
        await bot.send_message(
                message.chat.id,
                cap.reg_in_pride_bot
        )
    else:
        checker_sicret = get_user_data(
            message.from_user.id
        )
        if checker_sicret:            
            await bot.send_message(
                message.from_user.id,
                cap.tap_reserv,
                reply_markup=reserv_kb()
            )
        else:
            await bot.send_message(
                message.from_user.id,
                cap.start_msg,
                reply_markup=subscribe_to_bot_kb(
                    checker_pride
                )
            )


@dp.callback_query_handler(lambda callb: 'subscribe' in callb.data)
async def sub_p(call: types.CallbackQuery):
    text_user = cap.info_about_user_for_user(
        call.data.split('_', 1)[1]
    )
    text_admin = cap.info_about_user_for_admin(
        call.data.split('_', 1)[1]
    )
    kb_user = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text='Заявка успішно відпрвленна ✅',
            callback_data='0'
        )
    )
    kb_admin = admin_invite_kb(
        call.from_user.id,
        call.from_user.username
    )

    await bot.edit_message_text(
        text_user,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb_user
    )
    await bot.send_message(
        CHECK_GROUP,
        text_admin,
        reply_markup=kb_admin
    )


@dp.callback_query_handler(lambda calld: 'approve' in calld.data)
async def admin_answer(call: types.CallbackQuery):
    user_tg = call.data.split('_')[1]
    await bot.send_photo(
        user_tg,
        APPROVE_PHOTO
    )
    await bot.send_message(
        user_tg,
        cap.resers_acses
    )
    insert_new_user(user_tg)
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text = 'Доступ наданий ✅',
            callback_data='0'
        )
    )
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )


@dp.callback_query_handler(lambda calld: 'cancel' in calld.data)
async def admin_answer(call: types.CallbackQuery):
    user_tg = call.data.split('_')[1]
    await bot.send_message(
        user_tg,
        cap.resers_cancel
    )
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text = 'В доступі відхилино ❌',
            callback_data='0'
        )
    )
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )


class FSMReserv(StatesGroup):
    date = State()
    room = State()
    amount = State()


@dp.callback_query_handler(text='make_res')
async def make_register(call: types.CallbackQuery, state=FSMContext):
    await FSMReserv.date.set()
    await bot.edit_message_text(
        cap.date_res,
        call.message.chat.id,
        call.message.message_id
    )


@dp.message_handler(state=FSMReserv.date)
async def load_landlord_1(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await FSMReserv.next()
    await bot.send_message(
        message.chat.id,
        cap.room_res,
        reply_markup=room_kb()
    )


@dp.callback_query_handler(state=FSMReserv.room)
async def room11(call: types.CallbackQuery, state=FSMContext):
    if call.data == 'premium':
        async with state.proxy() as data:
            data['room'] = 'PREMIUM'
    elif call.data == 'vip':
        async with state.proxy() as data:
            data['room'] = 'VIP'       
    elif call.data == 's_vip':
        async with state.proxy() as data:
            data['room'] = 'SUPER VIP'
    elif call.data == 'streaming':
        async with state.proxy() as data:
            data['room'] = 'STREAMING'
    elif call.data == 'luxe':
        async with state.proxy() as data:
            data['room'] = 'LUXE'
    await FSMReserv.next()
    await bot.send_message(
        call.message.chat.id,
        cap.amount_res
    )


@dp.message_handler(state=FSMReserv.amount)
async def amount(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await bot.send_message(
        message.chat.id,
        cap.msg_with_room_for_user(
            data['date'], data['room'],
            data['amount'], 1
        ),
    )
    await bot.send_message(
        CHECK_GROUP,
        cap.msg_with_room_for_user(
            data['date'], data['room'],
            data['amount'], 2, 
            message.from_user.id
        ),
        reply_markup = admin_kb(
            message.from_user.username
        )
    )
    await state.finish()


@dp.callback_query_handler(text= 'res_plus')
async def approve_reserv(call: types.CallbackQuery):
    row_list = call.message.text.splitlines()
    tg_id = str(row_list[0])
    date = row_list[-3].split(':')[1].rstrip(' ')
    zone = row_list[-2].split(':')[1].rstrip(' ')
    amount = row_list[-1].split(':')[1].rstrip(' ')
    login = check_user_in_prideDB(tg_id)
    path = get_photo_from_card(
        login, date, zone, amount
    )
    photo = InputFile(path)
    await bot.send_photo(
        tg_id,
        photo,
        cap.reserv_approve_1(
            tg_id,
            date
        )
    )
    approve_reserv_db(
        int(tg_id), date, zone, amount
    )
    os.remove(path)
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text = 'Резерв подтверждён ✅',
            callback_data='0'
        )
    )
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )
    await call.answer(
        'Резерв підтвердженно'
    )


@dp.callback_query_handler(text= 'res_minus')
async def cancel_reserv(call: types.CallbackQuery):
    row_list = call.message.text.splitlines()
    tg_id = str(row_list[0])
    await bot.send_message(
        tg_id,
        cap.reserv_dab
    )
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text = 'Резерв відхиленно ❌',
            callback_data='0'
        )
    )
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )
    await call.answer(
        'Резерв відхиленно'
    )


@dp.callback_query_handler(text= 'sold_out')
async def cancel11_reserv(call: types.CallbackQuery):
    row_list = call.message.text.splitlines()
    tg_id = str(row_list[0])
    await bot.send_message(
        tg_id,
        cap.sold_out
    )
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text = 'Резерв відхиленно ❌',
            callback_data='0'
        )
    )
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )
    await call.answer(
        'Резерв відхиленно'
    )


@dp.callback_query_handler(text= 'more_hum')
async def cancel111_reserv(call: types.CallbackQuery):
    row_list = call.message.text.splitlines()
    tg_id = str(row_list[0])
    await bot.send_message(
        tg_id,
        cap.more_hum
    )
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text = 'Резерв відхиленно ❌',
            callback_data='0'
        )
    )
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )
    await call.answer(
        'Резерв відхиленно'
    )

# @dp.message_handler()
# async def get_msg_data(message: types.Message):
#     await bot.send_message(
#         message.chat.id,
#         message
#     )

@dp.message_handler(commands='list')
async def admin_list(message: types.Message):
    
    users_list = all()
    msg = ''
    count = 1
    
    premium = 0
    vip = 0
    s_vip = 0
    smtreaming = 0
    luxe = 0

    for user in users_list:
        if user[3] == ' PREMIUM':
            premium += 1 * int(user[4])
        elif user[3] == ' VIP':
            vip += 1 * int(user[4])
        elif user[3] == ' SUPER VIP':
            s_vip += 1 * int(user[4])

    msg += f'PREMIUM: {str(premium)} \\ 20\
        \nVIP: {str(vip)} \\ 10\
        \nSUPER VIP: {str(s_vip)} \\ 5\
        \nSTREAM: {str(smtreaming)} \\ 1\
        \nLUXE: {str(luxe)} \\ 1\n\n'

    for user in users_list:
        login = check_user_in_prideDB(user[1])
        msg += f'{count}| {login} |{user[2]} |{user[3]} |{user[4]} чел.\n\n'
        count += 1

    await bot.send_message(
        message.chat.id,
        msg
    )


@dp.message_handler(lambda msg: 'date' in msg.text)
async def plane_msg(messgae: types.Message):
    date = messgae.text.split(' ')[1]
    tg_id_list = secret_users()
    msg = f'🤫 Вітаємо, друже, у нас для Тебе є неймовірна новина!\
        \n\n{date} ми плануємо таємну зустріч у PRIDE. Для того, щоб це здійснилося, не вистачає САМЕ ТЕБЕ🔥\
        \n\nТож не зволікай, та тисни 👇🏻'
    rm_kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text='Хочу до вас!!!',
            callback_data=f'date_{date}'
        )
    )
    for user_id in tg_id_list:
        try:
            await bot.send_photo(
                user_id,
                "AgACAgIAAxkBAAIDAWO68bOAWvyVqDXxvWg6gO8UHBXVAAIlwTEbXBzZSQnbziBGnZZFAQADAgADeQADLQQ",
                caption = msg,
                reply_markup=rm_kb
            )
        except:
            continue


class FSMReserv1(StatesGroup):
    room = State()
    amount = State()


@dp.callback_query_handler(lambda callb: 'date' in callb.data)
async def admin_make_date(call: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        data['date'] = call.data.split('_')[1]
    await FSMReserv1.room.set()
    await bot.send_message(
        call.message.chat.id,
        cap.room_res,
        reply_markup=room_kb()
    )
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(state=FSMReserv1.room)
async def room111(call: types.CallbackQuery, state=FSMContext):
    if call.data == 'premium':
        async with state.proxy() as data:
            data['room'] = 'PREMIUM'
    elif call.data == 'vip':
        async with state.proxy() as data:
            data['room'] = 'VIP'       
    elif call.data == 's_vip':
        async with state.proxy() as data:
            data['room'] = 'SUPER VIP'
    await FSMReserv1.next()
    await bot.send_message(
        call.message.chat.id,
        cap.amount_res
    )
    await bot.answer_callback_query(call.id)


@dp.message_handler(state=FSMReserv1.amount)
async def amount1(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await bot.send_message(
        message.chat.id,
        cap.msg_with_room_for_user(
            data['date'], data['room'],
            data['amount'], 1
        ),
    )
    await bot.send_message(
        CHECK_GROUP,
        cap.msg_with_room_for_user(
            data['date'], data['room'],
            data['amount'], 2, 
            message.from_user.id
        ),
        reply_markup = admin_kb(
            message.from_user.username
        )
    )
    await state.finish()


@dp.message_handler(commands='users')
async def all_users_1(message: types.Message):
    
    user_list = all_tg_id()
    msg = ''
    count = 1

    for id in user_list:
        login = check_user_in_prideDB(id)
        msg += f'\n{count} | {login}'
        count += 1

    await bot.send_message(
        message.chat.id,
        msg
    )


#@dp.message_handler(content_types='photo')
#async def photo_id(message: types.Message):
#    await bot.send_message(
#        message.chat.id,
#        message
#    )


#@dp.message_handler(commands='enou')
#async def all_users_123(message: types.Message):
#    tg_id_list = secret_users()
#    msg = f'🚨ПОТРІБНА ТВОЯ ДОПОМОГА🚨\
#          \n13 січня 2023 року ми запланували таємну зустріч в PRIDE🧡\
#        \n\nДля того, щоб зустріч відбулась потрібно щоб Ти запросив ще кілька друзів🔥\
#          \nМи дуже хочемо зустрітись, але покищо гостей, які запланували візит, дуже мало.\
#        \n\nЗнаєш кого покликати? 🧡🧡🧡'
#    rm_kb = InlineKeyboardMarkup().add(
#        InlineKeyboardButton(
#            text='Резерв',
#            callback_data=f'date_13.01.2023'
#        )
#    )
#    for user_id in tg_id_list:
#        try:
#            await bot.send_message(
#                user_id,
#                msg,
#                reply_markup=rm_kb
#            )
#        except:
#            continue

    
