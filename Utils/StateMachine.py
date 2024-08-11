from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    # Блок сбора данных от юзера
    height_state = State()
    weight_state = State()
    age_state = State()
    sex_state = State()
    activity_state = State()
    # -----

    # Блок подписки и имейла
    is_subscribed = State()
    is_email = State()
    email_checking = State()
    email_right = State()
    email_exit = State()
    # -----
    send_email_wo_bonus = State()

    select_gift_yes = State()

    # Альтернативный вход во вторую ветку с бонусами
    alt_start = State()
    alt_sell = State()

    declaration = State()
    declaration_2 = State()
    declaration_3 = State()
    declaration_4 = State()
    declaration_5 = State()
    declaration_6 = State()

    start_select_bonus = State()
    select_gift = State()

    sell_0 = State()
    sell_1 = State()
    sell_2 = State()
    sell_3 = State()
    sell_4 = State()
    sell_5 = State()
    sell_6 = State()
    reply_1 = State()
    reply_2 = State()
    reply_3 = State()

    admin = State()

    promocode = State()
