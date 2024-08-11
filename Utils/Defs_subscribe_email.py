# # -----------------------------------------------------------------------------------
# # Блок проверки подписки и имейла
# from aiogram import Bot
# from aiogram.fsm.context import FSMContext
# from aiogram.types import CallbackQuery, Message
#
# from Config.config import CHANNEL_FOR_CHECKING
# from Keyboards.Inline_Keyboards import kb_9, kb_41, kb_5
# from Keyboards.Reply_Keyboards import r_kb_5
# from Utils.Check_is_email import is_email_correct
# from Utils.DB import update_values_db, get_max_id, request_to_db_column
# from Utils.Defs import send_email_wo_bonus, select_gift_yes
# from Utils.StateMachine import States
#
#
# async def subscribing(call: CallbackQuery, state: FSMContext, bot: Bot):
#     data = await state.get_data()
#     user_id_here = data['user_id']
#
#     tmp = await bot.get_chat_member(CHANNEL_FOR_CHECKING, user_id_here)
#     if tmp.status == 'left':
#         await bot.send_message(call.message.chat.id,
#                                "Ой! Я вижу Вы ещё не подписаны на чудесный канал '[Королевы Калорий 👑]("
#                                "https://t.me/+Vx6aUW5AO6U5M2U0)'!\nСкорее подпишитесь, а я Вас пока подожду!",
#                                disable_web_page_preview=True, parse_mode='Markdown', reply_markup=kb_5)
#         if call.data == 'subscribed':
#             tmp = await bot.get_chat_member(CHANNEL_FOR_CHECKING, user_id_here)
#             if tmp.status != 'left':
#                 await state.update_data(state_of_use='5_подписан')
#                 data = await state.get_data()
#                 list_values_of_DB = f"state_of_use = '{data['state_of_use']}'"
#                 update_values_db(list_values_of_DB, get_max_id(data['user_id']))
#
#                 await getting_email(call, state, bot)
#     else:
#         await state.update_data(state_of_use='5_подписан')
#         data = await state.get_data()
#         list_values_of_DB = f"state_of_use = '{data['state_of_use']}'"
#         update_values_db(list_values_of_DB, get_max_id(data['user_id']))
#
#         await getting_email(call, state, bot)
#
#
# async def getting_email(call: CallbackQuery, state: FSMContext, bot: Bot):
#     data = await state.get_data()
#     user_id_here = data['user_id']
#     request = await is_email_in_DB(user_id_here)
#     if request == '0':
#         await bot.send_message(call.message.chat.id, "🔸 Напишите мне свой имейл чтобы получить результаты",
#                                parse_mode='MarkDown', reply_markup=r_kb_5)
#         await state.set_state(States.email_checking)
#
#         await state.update_data(state_of_use='6_старт_запроса_имейла')
#         data = await state.get_data()
#         list_values_of_DB = f"state_of_use = '{data['state_of_use']}', gift = '{data['gift']}'"
#         id_in_base = get_max_id(data['user_id'])
#         update_values_db(list_values_of_DB, id_in_base)
#
#     else:
#         is_correct = is_email_correct(request)
#         if is_correct:
#             await bot.send_message(call.message.chat.id, f"➡️ Давайте проверим: Ваш email {request}", reply_markup=kb_9)
#             await state.update_data(email=request)
#             await state.set_state(States.email_right)
#
#
# async def email_checking(message: Message, state: FSMContext, bot: Bot):
#     if message.text != 'Без имейла':
#         is_correct = is_email_correct(message.text)
#         if is_correct:
#             await message.answer(f"➡️ Давайте проверим: Ваш email {message.text}", reply_markup=kb_9)
#             await state.update_data(email=message.text)
#             await state.set_state(States.email_right)
#         else:
#             await message.answer(f"Какая-то ошибка, давайте ещё раз!\nНапишите мне имейл", reply_markup=None)
#     else:
#         await message.answer(f"Вы уверены, что не хотите получить на имейл результаты?", reply_markup=kb_41)
#         await state.set_state(States.email_right)
#
#
# async def end_of_email(call: CallbackQuery, state: FSMContext, bot: Bot):
#     button = call.data
#     if button == 'right_email':
#         await state.update_data(state_of_use='7_имейл_получен')
#         data = await state.get_data()
#         list_values_of_DB = f"state_of_use = '{data['state_of_use']}', email = '{data['email']}'"
#         id_in_base = get_max_id(data['user_id'])
#         update_values_db(list_values_of_DB, id_in_base)
#
#         # !!! Точка выхода 1!!!
#         await state.set_state(States.email_exit)
#         await exit_email(call, state, bot)
#
#     elif button == 'without_email':
#         await state.update_data(state_of_use='7_без_имейла')
#         await state.update_data(is_email='wo_email')
#         # await state.update_data(wo_email='wo_email')
#         data = await state.get_data()
#         list_values_of_DB = f"state_of_use = '{data['state_of_use']}', is_email = 'wo_email'"
#         id_in_base = get_max_id(data['user_id'])
#         update_values_db(list_values_of_DB, id_in_base)
#
#         # !!! Точка выхода 2!!!
#         await state.set_state(States.email_exit)
#         await exit_email(call, state, bot)
#
#     elif button == 'wrong_email':
#         await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
#         await bot.send_message(call.message.chat.id, "🔸 Напишите мне свой имейл",
#                                parse_mode='MarkDown', reply_markup=None)
#         await state.set_state(States.email_checking)
#
#
# async def exit_email(call, state, bot):
#     data = await state.get_data()
#     exit_here = data['exit_email']
#     if exit_here == 1:
#         await state.set_state(States.send_email_wo_bonus)
#         await send_email_wo_bonus(call, state, bot)
#     elif exit_here == 2:
#         await state.set_state(States.select_gift_yes)
#         await select_gift_yes(call, state, bot)
#
#
# async def is_email_in_DB(user_id):
#     # Проверяем есть ли в базе имейл
#     was_email_received = '0'
#     xxx = request_to_db_column('email', 'user_id', user_id)
#     for x in tuple(xxx):
#         for v in x:
#             v = str(v)
#             if v != 'None':
#                 was_email_received = v
#                 break
#     return was_email_received
