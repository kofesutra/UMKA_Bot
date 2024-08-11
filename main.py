import asyncio
import contextlib
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.filters import Text, Command
from aiogram.types import BotCommand
from aiogram import F

from Utils.Defs_alt_enter import start_alt_enter, alt_sell
from Utils.Defs_get_user_measures import get_height, get_age, get_sex, get_activity, get_weight
from Utils.StateMachine import States
from Utils.Defs import on_start, run_declaration_2, run_declaration_3, get_support, select_gift, \
    run_sell_1, run_sell_2, run_sell_3, run_sell_4, run_sell_5, \
    run_sell_6, run_reply_1, run_reply_2, run_declaration, get_promocode, run_select_bonus, send_email_wo_bonus, \
    select_gift_yes, run_sell_0, subscribing, getting_email, email_checking, end_of_email, exit_email
from Config.config import BOT_TOKEN, ADMIN_ID, BOTUSERNAME
from Utils.Defs_admin import on_start_admin, run_db_export, run_db_export_short, run_ping_bot


async def start_bot(bot: Bot):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот остановлен')


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Старт"),
    ]
    await bot.set_my_commands(commands)


async def start():
    logging.basicConfig(level=logging.INFO,  # WARNING INFO
                        # filename="Logs/UMKA.log",
                        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                        datefmt='%H:%M:%S',
                        )
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(on_start, Command(commands=['start']))
    dp.message.register(on_start, Text(text='Начать заново'))
    dp.message.register(get_support, Text(text='Техподдержка'))

    dp.message.register(on_start_admin, Command(commands=['start']))
    dp.message.register(on_start_admin, Text(text='Начать заново'))
    dp.message.register(run_db_export, Text(text='База Полная'))
    dp.message.register(run_db_export_short, Text(text='База Краткая'))
    dp.message.register(run_ping_bot, Text(text='PING'))

    dp.message.register(get_height, States.height_state)
    dp.message.register(get_weight, States.weight_state)
    dp.message.register(get_age, States.age_state)
    dp.callback_query.register(get_sex, States.sex_state, F.data == 'female')
    dp.callback_query.register(get_sex, States.sex_state, F.data == 'male')
    dp.callback_query.register(get_activity, States.activity_state, F.data == 'activity_1')
    dp.callback_query.register(get_activity, States.activity_state, F.data == 'activity_2')
    dp.callback_query.register(get_activity, States.activity_state, F.data == 'activity_3')
    dp.callback_query.register(get_activity, States.activity_state, F.data == 'activity_4')
    dp.callback_query.register(get_activity, States.activity_state, F.data == 'activity_5')

    # Проверка подписки и имейла
    dp.callback_query.register(subscribing, States.is_subscribed)
    dp.message.register(getting_email, States.is_email)
    dp.message.register(email_checking, States.email_checking)
    dp.callback_query.register(end_of_email, States.email_right, F.data == 'right_email')
    dp.callback_query.register(end_of_email, States.email_right, F.data == 'wrong_email')
    dp.callback_query.register(end_of_email, States.email_right, F.data == 'without_email')
    dp.callback_query.register(exit_email, States.email_exit)
    dp.callback_query.register(send_email_wo_bonus, States.send_email_wo_bonus)

    dp.callback_query.register(run_declaration, States.declaration, F.data == 'next')
    dp.callback_query.register(run_declaration_2, States.declaration_2, F.data == 'declaration_on_2')
    dp.callback_query.register(run_declaration_3, States.declaration_3, F.data == 'declaration_on_3')
    dp.callback_query.register(run_declaration_3, States.declaration_3, F.data == 'next_sell')
    dp.callback_query.register(run_declaration_3, States.declaration_3, F.data == 'all_bonuses')

    dp.callback_query.register(run_select_bonus, States.start_select_bonus)
    dp.callback_query.register(select_gift, States.select_gift, F.data == '1')
    dp.callback_query.register(select_gift, States.select_gift, F.data == '2')
    dp.callback_query.register(select_gift, States.select_gift, F.data == '3')
    dp.callback_query.register(select_gift, States.select_gift, F.data == '4')
    dp.callback_query.register(select_gift, States.select_gift, F.data == '5')
    dp.callback_query.register(select_gift, States.select_gift, F.data == '6')
    dp.callback_query.register(select_gift, States.select_gift, F.data == '7')
    dp.callback_query.register(select_gift, States.select_gift, F.data == '8')
    dp.callback_query.register(select_gift, States.select_gift, F.data == '9')
    dp.callback_query.register(select_gift, States.select_gift, F.data == '10')
    dp.callback_query.register(select_gift, States.select_gift, F.data == 'yes')
    dp.callback_query.register(select_gift, States.select_gift, F.data == 'no')

    dp.callback_query.register(select_gift_yes, States.select_gift_yes)

    dp.callback_query.register(alt_sell, States.alt_sell)

    dp.callback_query.register(run_sell_0, States.sell_0)
    dp.callback_query.register(run_sell_1, States.sell_1)
    dp.callback_query.register(run_sell_2, States.sell_2, F.data == 'yes')
    dp.callback_query.register(run_sell_3, States.sell_3, F.data == 'next')
    dp.callback_query.register(run_sell_4, States.sell_4, F.data == 'next')
    dp.callback_query.register(run_sell_5, States.sell_5, F.data == 'replies')
    dp.callback_query.register(run_sell_5, States.sell_5, F.data == 'inside')

    dp.callback_query.register(run_sell_6, States.sell_6, F.data == 'buy_book')
    dp.callback_query.register(run_sell_6, States.sell_6, F.data == 'buy_book_promo')
    dp.callback_query.register(run_sell_6, States.sell_6, F.data == 'buy_bonuses')
    dp.callback_query.register(run_sell_6, States.sell_6, F.data == 'list_bonuses')
    dp.callback_query.register(run_sell_6, States.sell_6, F.data == 'promocode')

    dp.callback_query.register(run_reply_1, States.reply_1, F.data == 'more')
    dp.callback_query.register(run_reply_2, States.reply_2, F.data == 'more')

    dp.message.register(get_promocode, States.promocode)

    dp.message.register(start_alt_enter, States.alt_start)

    await set_commands(bot)  # Установка команд бота

    try:
        logging.error(f'OK - - - - - - - - - - - - - - - - - - - - OK\n\n'
                      f'[{BOTUSERNAME} started successful]: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', exc_info=True)
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())
