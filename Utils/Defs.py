import asyncio
import datetime

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from Calculation.Calc_reports import calc_1_report, calc_2_report, calc_3_report, calc_5_report, calc_4_report
from Email.Sending_email import sending_email_pdf, sending_email_wo_pdf, sending_email_alt_pdf
from Textes.List_of_Bonuses import list_of_bonuses, bonus_1, bonus_2, bonus_3, bonus_4, bonus_5, bonus_6, bonus_7, \
    bonus_8, bonus_9, bonus_10, list_of_bonuses_2
from Textes.Text_IMT import interpretation_1
from Keyboards.Inline_Keyboards import kb_5, kb_14, \
    kb_15, kb_24, kb_25, kb_28, kb_29, kb_30, kb_31, kb_33, kb_34, kb_9, \
    get_keyboard_37, kb_38, kb_39, kb_40, kb_35_1, get_keyboard_23, get_keyboard_23_2, kb_41, kb_43, get_keyboard_37_1, \
    get_keyboard_37_2
from Keyboards.Reply_Keyboards import r_kb_1, r_kb_5
from Utils.Check_bonuses import check_bonus_sended
from Utils.Check_is_email import is_email_correct
from Utils.DB import add_all_to_db, update_values_db, get_max_id, request_to_db_column
from Utils.Deeplinks import process_deeplinks
from Utils.Defs_alt_enter import start_alt_enter, alt_sell
from Utils.Process_invite_link import process_invite_link
from Utils.StateMachine import States
from Config.config import NAME_FOR_BASE, LIST_ADMINS, PROMOCODE, CHANNEL_FOR_CHECKING, BOT_URL, BOT_URL_INVITE
from datetime import datetime

from Utils.Defs_admin import on_start_admin


async def on_start(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    user_id_here = message.from_user.id
    if user_id_here in LIST_ADMINS:  # Если вошёл админ, то показываем другой интерфейс
        await state.set_state(States.admin)
        await on_start_admin(user_id_here)
    else:
        await state.update_data(user_id=user_id_here)
        username_here = message.from_user.username
        if username_here is None:
            username_here = 'None'
        await state.update_data(username=username_here)
        first_name_here = message.from_user.first_name
        if first_name_here is None:
            first_name_here = 'None'
        await state.update_data(first_name=first_name_here)
        last_name_here = message.from_user.last_name
        if last_name_here is None:
            last_name_here = 'None'
        await state.update_data(last_name=last_name_here)
        await state.update_data(date=message.date)
        await state.update_data(which_bot=NAME_FOR_BASE)
        await state.update_data(state_of_use='1_запуск')
        await state.update_data(is_email='none')  # Нужно записать предварительно
        await state.update_data(user_id_inviter='none')  # Нужно записать предварительно
        await state.update_data(gift='None')  # Нужно записать предварительно

        # Обработка DeepLinks
        deep = await process_deeplinks(message.text, state, bot)
        # -----

        data = await state.get_data()
        date_time_2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id_inviter = data['user_id_inviter']

        list_subjects_of_DB = "user_id, username, first_name, last_name, date_of_use, which_bot, state_of_use, come_from, is_email"
        list_data_of_DB = f"{data['user_id']}, '{data['username']}', '{data['first_name']}', '{data['last_name']}', " \
                          f"'{date_time_2}', '{data['which_bot']}', '{data['state_of_use']}', '{data['come_from']}', '{data['is_email']}'"
        add_all_to_db(list_subjects_of_DB, list_data_of_DB)

        # Обработка DeepLinks продолжение
        if deep == 'альтернативный':
            await state.set_state(States.alt_start)
            await start_alt_enter(state, bot)

        elif deep == 'invitelink':
            data = await state.get_data()
            user_id_inviter = data['user_id_inviter']
            await process_invite_link(user_id_inviter, state, bot)

        # else:
        await message.answer_photo(FSInputFile("Media/KK_Bot_Ava.png"),
                                   "✋ Привет! Я УМКА-бот и Ваш помощник!.\n"
                                   f"Я готов рассчитать Ваш индекс массы тела, "
                                   f"идеальный вес, дневную норму калорий и кое-что ещё 🤓",
                                   disable_web_page_preview=True, parse_mode='Markdown',
                                   reply_markup=None)

        await asyncio.sleep(2)
        await message.answer("1️⃣ Пришлите мне свой рост в сантиметрах")
        await state.set_state(States.height_state)


async def run_select_bonus(call: CallbackQuery, state: FSMContext, bot: Bot):
    # !!!!! Проверка, был ли выслан подарок уже
    data = await state.get_data()
    user_id_here = data['user_id']

    is_bonus_selected, is_bonus_sended_by_email, is_bonus_sended_by_bot = await check_bonus_sended(user_id_here, state,
                                                                                                   bot)
    if is_bonus_sended_by_email == '0' and is_bonus_sended_by_bot == '0':
        await bot.send_message(call.message.chat.id,
                               f'🔴\nПока я считаю выберите подарок из списка ниже и я пришлю его Вам',
                               parse_mode='MarkDown', reply_markup=None)
        await asyncio.sleep(3)
        await bot.send_photo(call.message.chat.id, FSInputFile("Media/All.png"), caption=list_of_bonuses,
                             reply_markup=kb_24)
        await state.set_state(States.select_gift)
        await select_gift(call, state, bot)

        await state.update_data(state_of_use='3_старт_выбора_подарка')
        data = await state.get_data()
        list_values_of_DB = f"state_of_use = '{data['state_of_use']}'"
        id_in_base = get_max_id(data['user_id'])
        update_values_db(list_values_of_DB, id_in_base)

    else:
        # await state.set_state(States.send_email_wo_bonus)
        # await send_email_wo_bonus(call, state, bot)
        await state.update_data(exit_email=1)
        # await state.set_state(States.is_subscribed)
        # await subscribing(call, state, bot)

        data = await state.get_data()
        list_values_of_DB = f"is_email = 'wo_email'"
        id_in_base = get_max_id(data['user_id'])
        update_values_db(list_values_of_DB, id_in_base)

        await state.set_state(States.select_gift_yes)
        await select_gift_yes(call, state, bot)


async def send_email_wo_bonus(call, state, bot):
    data = await state.get_data()
    is_email = data['is_email']
    come_from = data['come_from']
    if come_from == 'альтернативный':
        await state.set_state(States.alt_sell)
        await select_gift(call, state, bot)
        await alt_sell(call, state, bot)
    else:
        if is_email != 'wo_email':
            await sending_email_wo_pdf(state)

        await state.set_state(States.declaration)
        await select_gift(call, state, bot)
        await run_declaration(call, state, bot)


async def select_gift(call: CallbackQuery, state: FSMContext, bot: Bot):
    comm_here = ''
    list_of_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    activ = call.data  # Получение коллбэка - кнопка с каким текстом нажата
    if activ in list_of_numbers:
        if activ == '1':
            comm_here = bonus_1
        if activ == '2':
            comm_here = bonus_2
        if activ == '3':
            comm_here = bonus_3
        if activ == '4':
            comm_here = bonus_4
        if activ == '5':
            comm_here = bonus_5
        if activ == '6':
            comm_here = bonus_6
        if activ == '7':
            comm_here = bonus_7
        if activ == '8':
            comm_here = bonus_8
        if activ == '9':
            comm_here = bonus_9
        if activ == '10':
            comm_here = bonus_10

        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        await bot.send_message(call.message.chat.id, f'Ваш выбор: "{comm_here}", верно?', parse_mode='MarkDown',
                               reply_markup=kb_25)
        await state.update_data(gift=str(activ))

        await state.update_data(state_of_use='4_выбран_подарок')
        data = await state.get_data()
        list_values_of_DB = f"state_of_use = '{data['state_of_use']}', gift = '{data['gift']}'"
        id_in_base = get_max_id(data['user_id'])
        update_values_db(list_values_of_DB, id_in_base)

    elif activ == 'yes':
        await state.update_data(exit_email=2)
        # await state.set_state(States.is_subscribed)
        # await subscribing(call, state, bot)

        await state.update_data(is_email='wo_email')
        # await state.update_data(wo_email='wo_email')
        data = await state.get_data()
        list_values_of_DB = f"is_email = 'wo_email'"
        id_in_base = get_max_id(data['user_id'])
        update_values_db(list_values_of_DB, id_in_base)

        await state.set_state(States.select_gift_yes)
        await select_gift_yes(call, state, bot)

    elif activ == 'no':
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        await bot.send_message(call.message.chat.id, "🟢 Хорошо, выберите другой подарок!",
                               reply_markup=None)
        await bot.send_message(call.message.chat.id, list_of_bonuses, parse_mode='MarkDown', reply_markup=kb_24)


async def select_gift_yes(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    is_email = data['is_email']
    come_from = data['come_from']
    if come_from == 'альтернативный':
        if is_email != 'wo_email':
            await sending_email_alt_pdf(state)
            await bot.send_message(call.message.chat.id, "Принято!", reply_markup=None)
        else:
            await bot.send_message(call.message.chat.id,
                                   "Вы получите свой подарок немножко позже, читайте далее",
                                   reply_markup=None)
        await asyncio.sleep(1)

        await state.set_state(States.alt_sell)
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        await alt_sell(call, state, bot)

    else:
        # if is_email != 'wo_email':
        #     await sending_email_pdf(state)
        #     await bot.send_message(call.message.chat.id, "Принято!", reply_markup=None)
        # else:
        # await bot.send_message(call.message.chat.id,
        #                            "Вы получите свой подарок немножко позже, читайте далее",
        #                            reply_markup=None)
        # await asyncio.sleep(1)

        await state.set_state(States.declaration)
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        await run_declaration(call, state, bot)


async def run_declaration(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    mess = calc_1_report(data['imt'])
    mess_2 = calc_2_report(data['perf_wei'])
    mess_3 = calc_3_report(data['norm_cal'], data['min_cal'])
    mess_4 = calc_4_report(data['water'])
    mess_5 = calc_5_report(data['protein'], data['fat'], data['carbohidrate'])

    await bot.send_photo(call.message.chat.id, FSInputFile("Media/KK_Bot_Results_3.png"),
                         caption="." + "\n" + mess + "\n" + "\n" + mess_2 + "\n" + "\n" + mess_3 + "\n" + "\n" + mess_4 + "\n" + "\n" + mess_5,
                         reply_markup=r_kb_1)

    await asyncio.sleep(3)

    # await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.message.chat.id, "🟠 КАК ПОНИМАТЬ И ИСПОЛЬЗОВАТЬ ПОЛУЧЕННЫЕ РЕЗУЛЬТАТЫ?", reply_markup=r_kb_1)

    await asyncio.sleep(1)
    await bot.send_message(call.message.chat.id, interpretation_1(IMT=data['imt']),
                           parse_mode='MarkDown', reply_markup=kb_14)
    await state.set_state(States.declaration_2)

    await state.update_data(state_of_use='10_показаны_результаты')
    data = await state.get_data()
    list_values_of_DB = f"state_of_use = '{data['state_of_use']}'"
    id_in_base = get_max_id(data['user_id'])
    update_values_db(list_values_of_DB, id_in_base)


async def run_declaration_2(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.message.chat.id, f"🟣\n*Метаболический обмен (ОМО)*\nУ нас получились две "
                                                 f"цифры:\n*Ваша дневная норма калорий ({data['norm_cal']} ккал)* - "
                                                 f"расcчитана в соответствии с уровнем вашей физической "
                                                 f"активности. \nЭто то количество калорий, которое Вы можете "
                                                 f"съесть, не боясь набрать лишний вес, т.к. они полностью "
                                                 f"израсходуются организмом.",
                           parse_mode='MarkDown', reply_markup=kb_15)
    await state.set_state(States.declaration_3)


async def run_declaration_3(call: CallbackQuery, state: FSMContext, bot: Bot):
    button = call.data
    if button == 'declaration_on_3':
        data = await state.get_data()
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        await bot.send_message(call.message.chat.id,
                               f"🔵\n*Ваш основной обмен ({data['min_cal']} ккал)* - такое количество "
                               f"калорий необходимо для поддержания только внутренних процессов "
                               f"организма. \nЕсли калорий будет поступать меньше, значит будут "
                               f"нарушаться обменные процессы, а метаболизм замедляться. \nЭто "
                               f"может провоцировать ухудшение вашего здоровья.\n\n"
                               f"🟢\n*Разница между двумя показателями* и есть тот безопасный "
                               f"дефицит калорий, который вы можете себе позволить худея "
                               f"без вреда для здоровья. \nВ Вашем случае это "
                               f"*{data['diff_cal']}  ккал*.",
                               parse_mode='MarkDown', reply_markup=kb_35_1)
    elif button == "next_sell":
        await state.set_state(States.sell_0)
        await run_sell_0(call, state, bot)


async def run_sell_0(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id_here = data['user_id']
    # await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    kb_here = get_keyboard_37_1(f'invitelink{user_id_here}')
    await bot.send_message(call.message.chat.id,
                           f'🟣 Поздравляю! У Вас появилась возможность совершенно бесплатно получить уникальную "Королевскую коллекцию" на условиях партнёрской программы:\n'
                           f'отправьте реферальную ссылку восьми друзьям и, как только они её активируют, эта коллекция станет Вашей!\n\n'
                           f'Вот Ваша ссылка: {BOT_URL}?start=invitelink{user_id_here}\n\n'
                           f'Вы можете скопировать её и отправить другу или нажмите кнопку "Отправить ссылку" или просто перешлите сообщение ниже:',
                           disable_web_page_preview=True, reply_markup=kb_here)
    await asyncio.sleep(2)
    await bot.send_message(call.message.chat.id,
                           f'🟣 Привет! Смотри какой классный бот: за минуту рассчитывает идеальный вес, норму калорий, белков, жиров, углеводов и воды и дарит подарки!\n'
                           f'{BOT_URL}?start=invitelink{user_id_here}', disable_web_page_preview=True, reply_markup=None)
    await asyncio.sleep(2)
    kb_here = get_keyboard_37_2(f'invitelink{user_id_here}')
    await bot.send_message(call.message.chat.id,
                           f'🟢 Нет желания ждать и хочется купить всю коллекцию сразу? Читайте дальше, будет отличное предложение!',
                           parse_mode='MarkDown', reply_markup=kb_here)

    # await asyncio.sleep(5)

    # await bot.send_photo(call.message.chat.id, FSInputFile("Media/All.png"), caption=list_of_bonuses_2,
    #                      reply_markup=kb_here)

    await state.update_data(state_of_use='7_предложение_всех_бонусов')
    await state.update_data(gift_friend='888')  # Отметка для того, чтобы в строке с этой записью собирать инвайт-линки
    data = await state.get_data()
    list_values_of_DB = f"state_of_use = '{data['state_of_use']}', gift_friend = '{data['gift_friend']}'"
    id_in_base = get_max_id(data['user_id'])
    update_values_db(list_values_of_DB, id_in_base)

    await state.set_state(States.sell_1)


async def run_sell_1(call: CallbackQuery, state: FSMContext, bot: Bot):
    # await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    await bot.send_message(call.message.chat.id,
                           f"🟣 Многие считают, что худеть - это долго, нудно и трудно, да ещё не даёт гарантии результата.\n\n"
                           f"Они, отчасти, могут быть правы. Такое случается с людьми, которые выбрали неподходящую, некомфортную диету.\n\n"
                           f"Само слово «диета» становится неприятным, как бы напоминающим о прошлых экспериментах над собой и неудачах. "
                           f"Повторяющихся раз за разом.\n\n"
                           f"Согласны? Бывает такое?",
                           parse_mode='MarkDown', reply_markup=kb_28)

    await state.update_data(state_of_use='11_начало_продажи')
    data = await state.get_data()
    list_values_of_DB = f"state_of_use = '{data['state_of_use']}'"
    id_in_base = get_max_id(data['user_id'])
    update_values_db(list_values_of_DB, id_in_base)

    await state.set_state(States.sell_2)


async def run_sell_2(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.message.chat.id,
                           f"🟣 Огромное количество широко разрекламированных методик заманивают в свои сети человека, "
                           f"навязывают ему такие способы, справиться с которыми может только тот, кто их сочинил. "
                           f"Хуже того, иногда эти теории просто небезопасны.\n\n"
                           f"Неверный выбор диеты почти гарантирует срыв и возвращение веса.А всё почему? Ответ уже был! Диета должна быть комфортной.\n\n"
                           f"Это значит:\n- лёгкой в выполнении\n- не требующей много времени на анализ и подсчёт\n- без больших финансовых затрат",
                           parse_mode='MarkDown', reply_markup=kb_29)
    await state.set_state(States.sell_3)


async def run_sell_3(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.message.chat.id,
                           f"🟣 Кто-то скажет:«это невозможно». И будет прав — просто в его жизни ещё не случилась методика «Три правила системного питания».\n\n"
                           f"Это не диета, как её понимают многие. Это простые и понятные принципы, которые органично войдут в Вашу жизнь.\n\n"
                           f"Все они основаны на новейших достижениях науки и рекомендациях Всемирной организации здравоохранения.\n\n"
                           f"Принципы, которые помогают человеку снизить вес, продлить жизнь и сохранить крепкое здоровье на долгие годы.",
                           parse_mode='MarkDown', reply_markup=kb_30)
    await state.set_state(States.sell_4)


async def run_sell_4(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.message.chat.id,
                           f"🟣 Вы легко освоите их, примените в своей жизни и поразитесь, насколько забота о своей красоте и стройности, "
                           f"о своём здоровье может и должна быть комфортной, лёгкой и органичной!\n\n"
                           f"Представьте себе:\n"
                           f"Вам не придётся менять в жизни почти ничего, но вес начнёт неуклонно снижаться.\n"
                           f"Скрупулёзный подсчёт калорий больше не нужен.\n"
                           f"Заниматься физкультурой Вы станете только для удовольствия, или не заниматься вовсе.\n"
                           f"С каждым днём зеркало будет радовать Вас отражением всё больше и больше.\n"
                           f"Вернутся лёгкость и удовольствие движения.\n\n"
                           f"И Вы этого достигнете в максимально удобном и комфортном режиме.",
                           parse_mode='MarkDown', reply_markup=kb_31)
    await state.set_state(States.sell_5)


async def run_sell_5(call: CallbackQuery, state: FSMContext, bot: Bot):
    button = call.data
    if button == 'replies':
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        await bot.send_message(call.message.chat.id,
                               f'🟠 Вот, например, что мне написала Надежда:\n'
                               f'"Я смогла, девочки! Смогла! Достала платье из шкафа, надела...\n'
                               f'Просто слёзы на глазах - словно я вернулась на много лет назад! '
                               f'В то время, когда я была совсем юной и стройной.\n'
                               f'И теперь я снова выгляжу также. Муж не даст соврать. '
                               f'Мне кажется, ему понравилось даже больше, чем мне )".',
                               parse_mode='MarkDown', reply_markup=kb_33)

        await state.update_data(state_of_use='12_старт_отзывы')
        data = await state.get_data()
        list_values_of_DB = f"state_of_use = '{data['state_of_use']}'"
        id_in_base = get_max_id(data['user_id'])
        update_values_db(list_values_of_DB, id_in_base)

        await state.set_state(States.reply_1)

    elif button == 'inside':
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        await bot.send_photo(call.message.chat.id, FSInputFile("Media/Oblozhka_5.png"),
                             caption=f'🟣 В книге Вы найдёте:\n\n🔹 Пошаговый план действий, который приведёт к 100% результату\n'
                                     f'🔹 Инструкцию по применению основ Системного питания (с приложениями)\n🔹'
                                     f' Варианты меню - завтраки, обеды, ужины, бутерброды\n'
                                     f'🔹 Справочник по калорийности основных продуктов питания (для самостоятельного составления меню)\n'
                                     f'🔹 Чек-лист по выбору продуктов "Что есть, чтобы похудеть"\n'
                                     f'🔹 ТОП 5 Ошибок правильного питания, которые мешают похудеть\n'
                                     f'Сегодня стоимость руководства "Три правила Системного Питания" всего *1750 рублей* (вместо 3350).\n'
                                     f'Вместе с руководством «Три правила системного питания» Вы получите все бонусы "Королевской коллекции" без дополнительной оплаты!\n\n'
                                     f'🟢 Или же Вы можете отдельно приобрести "Королевскую коллекцию" стоимостью 1200 всего за *390 рублей* и получите скидочный купон на покупку руководства «Три правила системного питания»',
                             parse_mode='MarkDown', reply_markup=kb_38)

        await state.update_data(state_of_use='13_что_внутри')
        data = await state.get_data()
        list_values_of_DB = f"state_of_use = '{data['state_of_use']}'"
        id_in_base = get_max_id(data['user_id'])
        update_values_db(list_values_of_DB, id_in_base)

        # Отправка бонуса юзеру в боте
        data = await state.get_data()
        user_id_here = data['user_id']

        is_bonus_selected, is_bonus_sended_by_email, is_bonus_sended_by_bot = await check_bonus_sended(user_id_here,
                                                                                                       state, bot)

        if is_bonus_sended_by_bot != 'by_bot':
            if is_bonus_selected != '0':
                await asyncio.sleep(5)
                await bot.send_document(user_id_here, FSInputFile(f"Attachments/{is_bonus_selected}.pdf"),
                                        caption=f'Кстати, высылаю Вам бонус, который Вы выбрали.',
                                        reply_markup=None)
                if is_bonus_sended_by_email == 'by_email':
                    await bot.send_message(call.message.chat.id, "📧 Письмо на имейл так же отправлено",
                                           reply_markup=None)
                await state.update_data(
                    gift_friend='888')  # Отметка для того, чтобы в строке с этой записью собирать инвайт-линки
                data = await state.get_data()
                list_values_of_DB = f"gift_sended = 'by_bot', gift_friend = '{data['gift_friend']}'"
                id_in_base = get_max_id(data['user_id'])
                update_values_db(list_values_of_DB, id_in_base)

        await state.set_state(States.sell_6)


async def run_reply_1(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.message.chat.id,
                           f'🟠 Или письмо Татьяны:\n"У меня хранится кожаный ремень, который я носила ещё десять лет назад.\n'
                           f'И та самая дырка, на которую я его застёгивала тогда, теперь моя цель.\n'
                           f'Я точно знаю, что застегну на неё ремень, ведь до неё осталась ещё только одна, а было четыре!'
                           f'До неё осталась только одна, а было четыре!\nЯ точно знаю, что смогу!"',
                           parse_mode='MarkDown', reply_markup=kb_33)
    await state.set_state(States.reply_2)


async def run_reply_2(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.message.chat.id,
                           f'🟠 Отзыв Анастасии:\n"2,5 месяца назад я поставила себе цель - '
                           f'похудеть к лету на 6 килограмм с помощью Трех правил Системного Питания. И ведь сработало! '
                           f'Получилось даже перевыполнить: было 72 кг, а стало 62!\n'
                           f'Не ожидала, что эта система питания окажется настолько эффективной!\n'
                           f'Я начинала применять эти правила, когда еще не знала своего метаболического обмена (УМКА бот еще не родился) '
                           f'оказалось, что я недоедала! Было удивительно не урезать себя в еде, а наоборот, добавлять!\n'
                           f'Особенно когда цифры на весах так радовали! В общем, не хожу, а летаю, вся такая довольная, чего и вам желаю!"',
                           parse_mode='MarkDown', reply_markup=kb_34)
    await state.set_state(States.sell_5)


async def run_sell_6(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    button = call.data
    data = await state.get_data()
    user_id_here = data["user_id"]

    await state.update_data(state_of_use='13_совершить_покупку')
    data = await state.get_data()
    list_values_of_DB = f"state_of_use = '{data['state_of_use']}'"
    id_in_base = get_max_id(data['user_id'])
    update_values_db(list_values_of_DB, id_in_base)

    if button == 'buy_book':
        kb_here = get_keyboard_23(f'invitelink{user_id_here}')
        await bot.send_message(call.message.chat.id,
                               f'🟢 Поздравляю! Вы сделали правильный выбор! Даже я — робот — это понимаю!\n\n'
                               f'🟢 Как совершить покупку:\n\n'
                               f'1. Если у Вас есть промокод, нажмите кнопку *Ввести промокод*\n2. Нажмите кнопку выбранного товара\n3. Вы попадёте в бот приёма платежа\n4. Запустите его нажав кнопку "Запустить"',
                               parse_mode='MarkDown', reply_markup=kb_here)

    elif button == 'buy_book_promo':
        data = await state.get_data()
        promo_switch = data['promo']
        if promo_switch == 1:
            kb_here = get_keyboard_23_2(f'invitelink{user_id_here}')
            await bot.send_message(call.message.chat.id,
                                   f'🟢 Поздравляю! Цена скорректирована с учётом промокода.\n\n'
                                   f'🟢 Как совершить покупку:\n\n'
                                   f'1. Нажмите кнопку выбранного товара\n2. Вы попадёте в бот приёма платежа\n3. Запустите его нажав кнопку "Запустить"',
                                   parse_mode='MarkDown', reply_markup=kb_here)
        else:
            kb_here = get_keyboard_23(f'invitelink{user_id_here}')
            await bot.send_message(call.message.chat.id,
                                   f'🟢 Как совершить покупку:\n\n'
                                   f'1. Если у Вас есть промокод, нажмите кнопку *Ввести промокод*\n2. Нажмите кнопку выбранного товара\n3. Вы попадёте в бот приёма платежа\n4. Запустите его нажав кнопку "Запустить"',
                                   parse_mode='MarkDown', reply_markup=kb_here)

        await state.update_data(state_of_use='9_конец')
        data = await state.get_data()
        list_values_of_DB = f"state_of_use = '{data['state_of_use']}'"
        id_in_base = get_max_id(data['user_id'])
        update_values_db(list_values_of_DB, id_in_base)

    elif button == 'list_bonuses':
        await bot.send_message(call.message.chat.id,
                               f'🟠 Вот список бонусов, которые Вы можете получить:', parse_mode='MarkDown',
                               reply_markup=None)
        await asyncio.sleep(2)
        await bot.send_photo(call.message.chat.id, FSInputFile("Media/All.png"), caption=list_of_bonuses_2,
                             reply_markup=kb_38)

    elif button == 'promocode':
        await state.set_state(States.promocode)
        await bot.send_message(call.message.chat.id,
                               f'🟠 Вышлите мне промокод', parse_mode='MarkDown', reply_markup=None)


async def get_promocode(message: Message, state: FSMContext, bot: Bot):
    promo_here = message.text
    if promo_here == PROMOCODE:
        await state.set_state(States.sell_6)
        await message.answer('🟠 Промокод принят!', reply_markup=kb_39)
        await state.update_data(promo=1)

        await state.update_data(state_of_use='14_промокод_принят')
        data = await state.get_data()
        list_values_of_DB = f"state_of_use = '{data['state_of_use']}'"
        id_in_base = get_max_id(data['user_id'])
        update_values_db(list_values_of_DB, id_in_base)

    else:
        await state.set_state(States.sell_6)
        await message.answer('🔴 Промокод неверный, попробуйте ещё раз', reply_markup=kb_40)
        await state.update_data(promo=0)


async def get_support(message: Message):
    await message.answer(
        f"🟠 Если возник какой-то вопрос задай его в боте\n[⚙️ Техподдержка](http://t.me/Queens_Support_bot) ",
        disable_web_page_preview=True, parse_mode='Markdown', reply_markup=None)


# # -----------------------------------------------------------------------------------
# # Блок проверки подписки и имейла

async def subscribing(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id_here = data['user_id']

    tmp = await bot.get_chat_member(CHANNEL_FOR_CHECKING, user_id_here)
    if tmp.status == 'left':
        await bot.send_message(call.message.chat.id,
                               "Ой! Я вижу Вы ещё не подписаны на чудесный канал '[Королевы Калорий 👑]("
                               "https://t.me/+Vx6aUW5AO6U5M2U0)'!\nСкорее подпишитесь, а я Вас пока подожду!",
                               disable_web_page_preview=True, parse_mode='Markdown', reply_markup=kb_5)
        if call.data == 'subscribed':
            tmp = await bot.get_chat_member(CHANNEL_FOR_CHECKING, user_id_here)
            if tmp.status != 'left':
                await state.update_data(state_of_use='5_подписан')
                data = await state.get_data()
                list_values_of_DB = f"state_of_use = '{data['state_of_use']}'"
                update_values_db(list_values_of_DB, get_max_id(data['user_id']))

                await getting_email(call, state, bot)
    else:
        await state.update_data(state_of_use='5_подписан')
        data = await state.get_data()
        list_values_of_DB = f"state_of_use = '{data['state_of_use']}'"
        update_values_db(list_values_of_DB, get_max_id(data['user_id']))

        await getting_email(call, state, bot)


async def getting_email(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id_here = data['user_id']
    # data = await state.get_data()
    # is_email = data['is_email']
    # come_from = data['come_from']
    # if come_from == 'альтернативный':
    request = await is_email_in_DB(user_id_here)
    if request == '0':
        await bot.send_message(call.message.chat.id, "🔸 Если Вы хотите сохранить и/или распечатать материалы, то напишите мне свой имейл.\nЕсли нет, то нажмите кнопку *Без имейла* внизу экрана",
                               parse_mode='MarkDown', reply_markup=r_kb_5)
        await state.set_state(States.email_checking)

        await state.update_data(state_of_use='6_старт_запроса_имейла')
        data = await state.get_data()
        list_values_of_DB = f"state_of_use = '{data['state_of_use']}', gift = '{data['gift']}'"
        id_in_base = get_max_id(data['user_id'])
        update_values_db(list_values_of_DB, id_in_base)

    else:
        is_correct = is_email_correct(request)
        if is_correct:
            await bot.send_message(call.message.chat.id, f"➡️ Давайте проверим: Ваш email {request}", reply_markup=kb_9)
            await state.update_data(email=request)
            await state.set_state(States.email_right)


async def email_checking(message: Message, state: FSMContext, bot: Bot):
    if message.text != 'Без имейла':
        is_correct = is_email_correct(message.text)
        if is_correct:
            await message.answer(f"➡️ Давайте проверим: Ваш email {message.text}", reply_markup=kb_9)
            await state.update_data(email=message.text)
            await state.set_state(States.email_right)
        else:
            await message.answer(f"Какая-то ошибка, давайте ещё раз!\nНапишите мне имейл", reply_markup=None)
    else:
        await message.answer(f"Вы уверены, что не хотите получить на имейл результаты?", reply_markup=kb_41)
        await state.set_state(States.email_right)


async def end_of_email(call: CallbackQuery, state: FSMContext, bot: Bot):
    button = call.data
    if button == 'right_email':
        # await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        await state.update_data(state_of_use='7_имейл_получен')
        data = await state.get_data()
        list_values_of_DB = f"state_of_use = '{data['state_of_use']}', email = '{data['email']}, is_email = 'with_email''"
        id_in_base = get_max_id(data['user_id'])
        update_values_db(list_values_of_DB, id_in_base)

        # !!! Точка выхода 1!!!
        await state.set_state(States.email_exit)
        await exit_email(call, state, bot)

    elif button == 'without_email':
        # await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        await state.update_data(state_of_use='7_без_имейла')
        await state.update_data(is_email='wo_email')
        # await state.update_data(wo_email='wo_email')
        data = await state.get_data()
        list_values_of_DB = f"state_of_use = '{data['state_of_use']}', is_email = 'wo_email'"
        id_in_base = get_max_id(data['user_id'])
        update_values_db(list_values_of_DB, id_in_base)

        # !!! Точка выхода 2!!!
        await state.set_state(States.email_exit)
        await exit_email(call, state, bot)

    elif button == 'wrong_email':
        # await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        await bot.send_message(call.message.chat.id, "🔸 Напишите мне свой имейл",
                               parse_mode='MarkDown', reply_markup=None)
        await state.set_state(States.email_checking)


async def exit_email(call, state, bot):
    data = await state.get_data()
    exit_here = data['exit_email']
    if exit_here == 1:
        await state.set_state(States.send_email_wo_bonus)
        await send_email_wo_bonus(call, state, bot)
    elif exit_here == 2:
        await state.set_state(States.select_gift_yes)
        await select_gift_yes(call, state, bot)


async def is_email_in_DB(user_id):
    # Проверяем есть ли в базе имейл
    was_email_received = '0'
    xxx = request_to_db_column('email', 'user_id', user_id)
    for x in tuple(xxx):
        for v in x:
            v = str(v)
            if v != 'None':
                was_email_received = v
                break
    return was_email_received
