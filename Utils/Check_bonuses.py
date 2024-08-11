from aiogram import Bot
from aiogram.fsm.context import FSMContext

from Utils.DB import request_to_db_column, request_to_db_column_two


async def check_is_deeplink_for_second_bonus(state: FSMContext, bot: Bot):
    data = await state.get_data()
    # user_id_for_second_bonus = data['second_bonus_to_user']
    user_id_for_second_bonus = data['user_id_inviter']
    # Проверяем, указанный юзер заказывал ли второй бонус
    # Если да, то получем номер бонуса и имейл

    was_second_bonus_sended = '0'
    yyy = request_to_db_column('gift_friend_sended', 'user_id', user_id_for_second_bonus)
    for x in tuple(yyy):  # Команда tuple превращает список в кортеж
        for v in x:
            v = str(v)
            if v != 'None':
                was_second_bonus_sended = v
                break

    was_second_bonus_requested = '0'
    id_for_work = '0'
    zzz = request_to_db_column('gift_friend', 'user_id', user_id_for_second_bonus)
    for x in tuple(zzz):  # Команда tuple превращает список в кортеж
        for v in x:
            v = str(v)
            if v != 'None':
                was_second_bonus_requested = v
                id_for_work = request_to_db_column_two('id', 'user_id', user_id_for_second_bonus, 'gift_friend', was_second_bonus_requested)
                break

    # Проверяем есть ли в базе имейл
    was_email_received = '0'
    xxx = request_to_db_column('email', 'user_id', user_id_for_second_bonus)
    for x in tuple(xxx):
        for v in x:
            v = str(v)
            if v != 'None':
                was_email_received = v
                break

    return was_second_bonus_sended, was_second_bonus_requested, was_email_received, id_for_work


async def check_bonus_sended(user_id_here, state: FSMContext, bot: Bot):
    # Проверяем, был ди юзером уже получен какой-либо бонус
    # Для этого проверяем есть ли в базе номер полученного подарка
    is_bonus_selected = '0'
    zzz = request_to_db_column('gift', 'user_id', user_id_here)
    for x in tuple(zzz):  # Команда tuple превращает список в кортеж
        for v in x:
            v = str(v)
            if v != 'None':
                is_bonus_selected = v
                break

    # Проверяем был ли выслан бонус
    is_bonus_sended_by_email = '0'
    is_bonus_sended_by_bot = '0'
    xxx = request_to_db_column('gift_sended', 'user_id', user_id_here)
    for x in tuple(xxx):
        for v in x:
            v = str(v)
            if v != 'None':
                if v == 'by_email':
                    is_bonus_sended_by_email = v
                if v == 'by_bot':
                    is_bonus_sended_by_bot = v
                break

    return is_bonus_selected, is_bonus_sended_by_email, is_bonus_sended_by_bot

