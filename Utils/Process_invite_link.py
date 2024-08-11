from Email.Sending_email import sending_email_personal_wo_pdf
from Email.email_all_bonuses import subject_email_all_bonuses, text_email_all_bonuses
from Keyboards.Inline_Keyboards import kb_42
from Utils.Check_bonuses import check_is_deeplink_for_second_bonus
from Utils.DB import update_values_db, request_to_db_column


async def process_invite_link(user_id_inviter, state, bot):
    # ID из ссылки (приглашающий) и текущего юзера не совпадают
    data = await state.get_data()
    user_id_here = data['user_id']
    if user_id_inviter != user_id_here:

        # Смотрим в базе: выслан ли второй бонус, выбран ли второй бонус, имеется ли имейл
        second_bonus_sended, second_bonus, email_to_send, id_for_work = await check_is_deeplink_for_second_bonus(
            state, bot)

        # Если бонус не выслан и выбран
        if second_bonus_sended == '0' and second_bonus != '0':

            # Проверить есть ли уже 8 подписок
            list_here = await check_invited_list(user_id_inviter, user_id_here)
            is_ten = list_here.count('_')

            # Проверяем, есть ли id приглашённого уже в списке пригласителя
            count_of_invited = list_here.count(str(user_id_here))
            if count_of_invited == 0:

                # Если текущая диплинка 8, то вносим юзера в базу,
                # высылаем бонус и ставим в базе отметку gift_friend_sended = sended
                if is_ten == 7:
                    if email_to_send != '0':
                        # Тема и текст письма в отдельном файле
                        await sending_email_personal_wo_pdf(email_to_send, subject_email_all_bonuses,
                                                            text_email_all_bonuses)

                    await bot.send_message(user_id_inviter,
                                           f'Полная "Королевская коллекция" бонусов за то, что пригласили друзей в УМКА-бот.\n\n'
                                           f'Переходите по ссылке смело! Благодарю за доверие!',
                                           reply_markup=kb_42)

                    zzz2 = str(str(list_here) + "_" + str(user_id_here))
                    list_values_of_DB = f"invited = '{zzz2}', gift_friend_sended = 'sended'"
                    id_in_base = id_for_work
                    update_values_db(list_values_of_DB, id_in_base)

                else:
                    zzz2 = str(str(list_here) + "_" + str(user_id_here))
                    list_values_of_DB = f"invited = '{zzz2}'"
                    id_in_base = id_for_work
                    update_values_db(list_values_of_DB, id_in_base)


async def check_invited_list(user_id_inviter, user_id_invited):
    list_here = ''
    yyy = request_to_db_column('invited', 'user_id', user_id_inviter)
    for x in tuple(yyy):  # Команда tuple превращает список в кортеж
        for v in x:
            if v is not None:
                if list_here == '':
                    list_here = v
                break
    return list_here
