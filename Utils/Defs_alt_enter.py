import asyncio

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, CallbackQuery

from Keyboards.Inline_Keyboards import kb_24, kb_43, get_keyboard_37
from Keyboards.Reply_Keyboards import r_kb_1
from Textes.List_of_Bonuses import list_of_bonuses
from Utils.Check_bonuses import check_bonus_sended
from Utils.DB import get_max_id, update_values_db
from Utils.StateMachine import States


# Блок альтернативного входа во вторую ветку с бонусами
async def start_alt_enter(state: FSMContext, bot: Bot):
    # !!!!! Проверка, был ли выслан подарок уже
    data = await state.get_data()
    user_id_here = data['user_id']

    is_bonus_selected, is_bonus_sended_by_email, is_bonus_sended_by_bot = await check_bonus_sended(user_id_here, state,
                                                                                                   bot)
    if is_bonus_sended_by_email == '0' and is_bonus_sended_by_bot == '0':
        await bot.send_message(user_id_here, '🌟 Узнайте тайны похудения вместе с нашей "Королевской коллекцией"!\n'
                                             'Мы приготовили для Вас невероятную коллекцию полезных материалов о похудении. Это настоящая сокровищница знаний!\n\n'
                                             '🔘 Хотите узнать, как полюбить свое тело и стать стройнее? Мы расскажем все секреты!\n'
                                             '🔘 Знаете, как справиться с обжорством и контролировать пищевую систему? Мы поделимся простыми и эффективными способами.\n'
                                             '🔘 Увлекательные идеи и лайфхаки для комфортного снижения веса. Это просто волшебно!\n'
                                             '🔘 И это еще не все! Мы поможем Вам активизировать омолаживающий процесс организма и даже улучшить самочувствие.\n\n'
                                             '🟢 Выбирайте понравившийся бонус и получите его *абсолютно бесплатно*!',
                             parse_mode='MarkDown', reply_markup=None)
        await asyncio.sleep(5)
        await bot.send_photo(user_id_here, FSInputFile("Media/All.png"), caption=list_of_bonuses,
                                   reply_markup=kb_24)
        await state.set_state(States.select_gift)

        await state.update_data(state_of_use='альт_старт_выбора_подарка')
        data = await state.get_data()
        list_values_of_DB = f"state_of_use = '{data['state_of_use']}'"
        id_in_base = get_max_id(data['user_id'])
        update_values_db(list_values_of_DB, id_in_base)

    else:
        await bot.send_message(user_id_here, '🌟 Узнайте тайны похудения вместе с нашей "Королевской коллекцией"!\n'
                                             'Мы приготовили для Вас невероятную коллекцию полезных материалов о похудении. Это настоящая сокровищница знаний!\n\n'
                                             '🔘 Хотите узнать, как полюбить свое тело и стать стройнее? Мы расскажем все секреты!\n'
                                             '🔘 Знаете, как справиться с обжорством и контролировать пищевую систему? Мы поделимся простыми и эффективными способами.\n'
                                             '🔘 Увлекательные идеи и лайфхаки для комфортного снижения веса. Это просто волшебно!\n'
                                             '🔘 И это еще не все! Мы поможем Вам активизировать омолаживающий процесс организма и даже улучшить самочувствие.\n\n'
                                             '🟢 Разве это не интересно?',
                             parse_mode='MarkDown', reply_markup=kb_43)
        await state.update_data(exit_email=1)
        await state.set_state(States.is_subscribed)


async def alt_sell(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id_here = data['user_id']
    # await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    await bot.send_message(call.message.chat.id,
                           f'🟣 Поздравляю! У Вас появилась возможность *совершенно бесплатно* получить уникальную "Королевскую коллекцию" на условиях партнёрской программы:\n\n'
                           f'отправьте реферальную ссылку *восьми* друзьям и, как только они её активируют, эта коллекция станет Вашей!\n\n'
                           f'🟢 Нет желания ждать и хочется купить всю коллекцию сразу? Читайте дальше, будет отличное предложение!',
                           parse_mode='MarkDown', reply_markup=r_kb_1)

    await asyncio.sleep(5)
    kb_here = get_keyboard_37(f'invitelink{user_id_here}')
    await bot.send_photo(call.message.chat.id, FSInputFile("Media/All.png"), reply_markup=kb_here)

    await state.update_data(state_of_use='альт_предложение_всех_бонусов')
    await state.update_data(gift_friend='888')  # Отметка для того, чтобы в строке с этой записью собирать инвайт-линки
    data = await state.get_data()
    list_values_of_DB = f"state_of_use = '{data['state_of_use']}', gift_friend = '{data['gift_friend']}'"
    id_in_base = get_max_id(data['user_id'])
    update_values_db(list_values_of_DB, id_in_base)

    await state.set_state(States.sell_1)
