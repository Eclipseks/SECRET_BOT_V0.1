from func.login import check_acs, check_all_amount
from base.base_db import check_user_in_prideDB

reg_in_pride_bot = 'Упс, щось пішло не так...\
                \nCпершу необхідно зареєструватися через основний бот за посиланням\
                \n\n<b>t.me/pride_gg_bot</b>'
start_msg = 'Таємно вітаємо Тебе в PRIDE SECRET ROOM\
        \nДля того, щоб приєднатися до нас, натисни 👇🏻'
resers_cancel = 'Не засмучуйся, можливо лише пара кроків відділяє тебе від бажаного, не втрачай надії.\
                \nЧекаємо на Тебе як завжди у PRIDE🔥'
resers_acses = 'Оуууу, Ти насправді особливий гість, Твій запит на вступ СХВАЛЕНО🔥\
            \nРаді вітати Тебе на темній стороні PRIDE🌚\
            \nТепер Ти частина нашої великої таємниці, а це не тільки наша спільна перевага, але й відповідальність, тому є кілька важливих моментів:\
            \n\n🔸Перше правило SECRET ROOM:\
            \nНіхто не має знати про SECRET ROOM....🤫\
            \n🔸Друге правило SECRET ROOM: \
            \nЗапросити нових учасників Ти можеш тільки під власну гарантію конфіденційності.\
            \n🔸Третє правило SECRET ROOM: \
            \nТільки «вхідний квиток» дає право на участь у заході. Початок зустрічі з 22:00 до 22:30, будь ласка, не запізнюйся.\
            \n🔸Четверте правило SECRET ROOM: \
            \nВсі зустрічі відбуватимуться у повністю зачиненому режимі до 5:00, але Ти маєш можливість бути з нами до 7:00.\
            \n🔸П‘яте правило SECRET ROOM:\
            \nПорушення будь-якого правила позбавляє Тебе права відвідувати PRIDE!\
            \n\nТож, давай почнемо, натисни /start'
tap_reserv = 'Давай разом зробимо резерв, тисни 👇🏻'
date_res = 'Відправ заплановану дату таємної зустрічі:'
room_res = 'Обери бажану зону:'
amount_res = 'Відправ кількість місць, які бажаєш забронювати:'
reserv_dab = 'Резерв відхилено'

sold_out = 'На цю дату немає вільних місць, але ще є шанс встигнути забронювати місця на інший день🧡'
more_hum = 'Покищо не можемо підтвердити Твій резерв, не зібралось достатньої кількості учасників. Запроси друзів і ми обов\'язково зустрінемося в цей день🔥'


def reserv_approve_1(tg_id, date):
    login = check_user_in_prideDB(str(tg_id))
    reserv_succsses = f'{login}, Резерв прийнято, це ТВІЙ БІЛЕТ у PRIDE, чекаємо на зустріч {date} о 22:00. 🧡'
    return reserv_succsses


def info_about_user_for_user(login):

    user_info = check_acs(login)
    visit_time = user_info['number_of_visits']
    amount = user_info['account_amount']

    msg = f'Вітаємо, {login}, заявка відправлена на розгляд, очікуй на відповідь..\
        \n\nДанні кандидата:\
        \n\nКількість відвідувань: {visit_time}\
        \nБаланс на аккаунті: {amount}'

    return msg


def info_about_user_for_admin(login):

    user_info = check_acs(login)
    visit_time = str(user_info['number_of_visits'])
    amount = user_info['account_amount']
    amount_info = check_all_amount(login) 

    msg = f'Нова заявка на вступ!!!\
        \n\nДанні профілю юзера:\
        \n\nЛогін: {login}\
        \n\nКількість відвідувань: {visit_time}\
        \nБаланс на аккаунті: {amount}\
        \nЗагальна сумма витрат: {amount_info}'
        
    return msg

def msg_with_room_for_user(date, room, amount, priority, tg = None):
    if priority == 1:
        msg = f'Резер на {date}\
        \n\nЗона: {room}\
        \nКількість людей: {amount}\
        \n\nДякуємо🧡 Заявка на резерв прийнята, очікуй на підтвердження...'
    else:
        login = check_user_in_prideDB(str(tg))
        msg = f'{tg}\
            \nНовый резерв!\
            \n\nLogin: {login}\
            \n\nДата: {date}\
            \nЗона: {room}\
            \nКоличество людей: {amount}'
    return msg
    
