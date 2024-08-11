import os
from _csv import writer
from datetime import datetime

from aiogram import Bot
from aiogram.types import FSInputFile, CallbackQuery

from Config.config import BOT_TOKEN, LIST_SUBJECTS, CSV_FILE, CSV_FILE_2, LIST_SUBJECTS_SHORT
from Keyboards.Reply_Keyboards import r_kb_admin
from Utils.DB import db_export, db_export_short

bot = Bot(token=BOT_TOKEN)


async def on_start_admin(user):
    await bot.send_message(user, f'Преведт, админ {user}!', reply_markup=r_kb_admin)


async def run_db_export(call: CallbackQuery):
    admin_here = call.from_user.id

    await bot.send_message(admin_here, 'Экспорт полной БД')
    zzz = db_export()

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_time_2 = str(date_time)
    csv_here = CSV_FILE + date_time_2 + '.csv'

    with open(csv_here, mode='a', encoding='utf-8', newline='') as file:
        writer_object = writer(file)
        writer_object.writerow(LIST_SUBJECTS)
        writer_object.writerows(zzz)
        file.close()

    await bot.send_document(admin_here, FSInputFile(f"{csv_here}"))

    os.remove(csv_here)


async def run_db_export_short(call: CallbackQuery):
    admin_here = call.from_user.id

    await bot.send_message(admin_here, 'Экспорт краткой БД')
    zzz = db_export_short()

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_time_2 = str(date_time)
    csv_here = CSV_FILE_2 + date_time_2 + '.csv'

    with open(csv_here, mode='a', encoding='utf-8', newline='') as file:
        writer_object = writer(file)
        writer_object.writerow(LIST_SUBJECTS_SHORT)
        writer_object.writerows(zzz)
        file.close()

    await bot.send_document(admin_here, FSInputFile(f"{csv_here}"))

    os.remove(csv_here)


async def run_ping_bot(call: CallbackQuery):
    admin_here = call.from_user.id
    await bot.send_message(admin_here, 'Я в норме! Я не сплю! )))')