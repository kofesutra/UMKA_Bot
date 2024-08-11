from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Calculation.Calculate import get_calculations
from Keyboards.Inline_Keyboards import kb_2, kb_4, kb_7
from Keyboards.Reply_Keyboards import r_kb_1
from Utils.Check_is_digits import check_digits
from Utils.Check_is_height import check_height, check_weight, check_age
from Utils.DB import get_max_id, update_values_db
from Utils.StateMachine import States


async def get_height(message: Message, state: FSMContext):
    dig_here = check_digits(message.text)
    dig_2_here = check_height(dig_here)
    if dig_here == 1639572 or dig_2_here == 0:
        await message.answer("1️⃣ Какая-то ошибка, давайте ещё раз!\nПришлите мне свой рост в сантиметрах")
    else:
        await state.update_data(height=dig_here)
        await state.set_state(States.weight_state)
        await message.answer("2️⃣ Пришлите мне свой вес в килограммах")


async def get_weight(message: Message, state: FSMContext):
    dig_here = check_digits(message.text)
    dig_2_here = check_weight(dig_here)
    if dig_here == 1639572 or dig_2_here == 0:
        await message.answer("️2️⃣ Какая-то ошибка, давайте ещё раз!\nПришлите мне свой вес в килограммах")
    else:
        await state.update_data(weight=dig_here)
        await state.set_state(States.age_state)
        await message.answer("3️⃣ Пришлите мне свой возраст")


async def get_age(message: Message, state: FSMContext):
    dig_here = check_digits(message.text)
    dig_2_here = check_age(dig_here)
    if dig_here == 1639572 or dig_2_here == 0:
        await message.answer("️3️⃣ Какая-то ошибка, давайте ещё раз!\nПришлите мне свой возраст")
    else:
        await state.update_data(age=dig_here)
        await state.set_state(States.sex_state)
        await message.answer("Ещё вопрос:", reply_markup=r_kb_1)
        await message.answer("4️⃣ Вы женщина или мужчина?", reply_markup=kb_2)


async def get_sex(call: CallbackQuery, state: FSMContext, bot: Bot):
    activ = call.data  # Получение коллбэка - кнопка с каким текстом нажата
    if activ == 'male':
        res_here = 'мужской'
    else:
        res_here = 'женский'

    await state.update_data(sex=res_here)
    await state.set_state(States.activity_state)
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.message.chat.id, "5️⃣ Укажите свой уровень физических нагрузок", reply_markup=kb_4)


async def get_activity(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.answer_callback_query(callback_query_id=call.id, text='', show_alert=False)

    activ = call.data  # Получение коллбэка - кнопка с каким текстом нажата
    if activ == 'activity_1':
        comm_here = "сидячая работа"
        res_here = 1
    elif activ == 'activity_2':
        comm_here = 'пробежки или гимнастика 1-3 раза в неделю'
        res_here = 2
    elif activ == 'activity_3':
        comm_here = 'спорт с нагрузками 3-5 раз в неделю'
        res_here = 3
    elif activ == 'activity_4':
        comm_here = 'полноценные тренировки 5-7 раз в неделю'
        res_here = 4
    else:
        comm_here = 'физический труд и силовые тренировки'
        res_here = 5
    await state.update_data(activity=res_here)
    # await state.set_state(States.user_datas)

    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    await state.update_data(state_of_use='2_опрошен')
    await get_calculations(state)
    data = await state.get_data()
    # Записываем данные в БД
    list_values_of_DB = f"height = {data['height']}, weight = {data['weight']}, age = {data['age']}, " \
                        f"sex = '{data['sex']}', activity = {data['activity']}, state_of_use = '{data['state_of_use']}'"
    id_in_base = get_max_id(data['user_id'])
    update_values_db(list_values_of_DB, id_in_base)

    await bot.send_message(call.message.chat.id, "✅ Давайте проверим введённые данные:\n" + "\n" +
                           f"✔️ рост - {data['height']} см\n"
                           f"✔️ вес - {data['weight']} кг\n"
                           f"✔️ возраст - {data['age']}\n"
                           f"✔️ пол - {data['sex']}\n"
                           f"✔️ активность - " + comm_here + "\n" + "\n" +
                           f"➡️ Все данные верны?",
                           parse_mode='MarkDown', reply_markup=kb_7)
    # await state.set_state(States.is_subscribed)  # Переходим к блоку проверки подписки и имейла
    await state.set_state(States.start_select_bonus)
