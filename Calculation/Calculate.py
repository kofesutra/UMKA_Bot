from datetime import datetime

from aiogram.fsm.context import FSMContext

from Calculation.Calc_reports import calc_1_report, calc_3_report, calc_4_report, calc_5_report, calc_2_report
from Utils.DB import get_max_id, update_values_db
from Utils.Write_to_CSV import write_to_csv


def calculations(WEIGHT, HEIGHT):
    # Индекс массы тела (индекс Кетле)
    result = round(WEIGHT / pow(HEIGHT / 100, 2), 2)
    return result


def calculations_2(HEIGHT, SEX):
    result: float = 0
    # Формула для расчета идеальной массы тела по методу Devine (чаще всего используется для расчета)
    if SEX == 'мужской':
        result = round(50 + 2.3 * (0.394 * HEIGHT - 60), 1)  # по методу Devine
    elif SEX == 'женский':
        result = round(45.5 + 2.3 * (0.394 * HEIGHT - 60), 1)
    return result


def calculations_3(WEIGHT, HEIGHT, AGE, SEX, ACTIVITY):
    report: str = ""
    coeff: float = 1
    if ACTIVITY == 1:
        coeff = 1.2
    elif ACTIVITY == 2:
        coeff = 1.375
    elif ACTIVITY == 3:
        coeff = 1.55
    elif ACTIVITY == 4:
        coeff = 1.725
    elif ACTIVITY == 5:
        coeff = 1.9
    else:
        coeff = 1

    result_1 = 0
    result_2 = 0
    if SEX == 'мужской':
        result_1 = round(((10 * WEIGHT) + (6.25 * HEIGHT) - (5 * AGE) + 5) * coeff)
        result_2 = round((10 * WEIGHT) + (6.25 * HEIGHT) - (5 * AGE) + 5)
    elif SEX == 'женский':
        result_1 = round(((10 * WEIGHT) + (6.25 * HEIGHT) - (5 * AGE) - 161) * coeff)
        result_2 = round((10 * WEIGHT) + (6.25 * HEIGHT) - (5 * AGE) - 161)
    return result_1, result_2


def calculations_4(WEIGHT):
    result = round((WEIGHT / 450) * 14, 1)  # Норма воды
    return result


def calculations_5(CCAL):
    # result_1 = round(WEIGHT * 0.8)
    # result_2 = round(WEIGHT * 1.2)
    result_1 = round((CCAL * 0.3) / 4)  # Белки
    result_2 = round((CCAL * 0.3) / 9)  # Жиры
    result_3 = round((CCAL * 0.4) / 4)  # Углеводы
    return result_1, result_2, result_3


async def get_calculations(state: FSMContext):
    data = await state.get_data()
    hei = float(data['height'])
    wei = float(data['weight'])
    ag = float(data['age'])
    sexx = str(data['sex'])
    act = int(data['activity'])

    imt = calculations(wei, hei)
    await state.update_data(imt=imt)
    mess = calc_1_report(imt)

    perf_wei = calculations_2(hei, sexx)
    await state.update_data(perf_wei=perf_wei)
    mess_2 = calc_2_report(perf_wei)

    norm_cal, min_cal = calculations_3(wei, hei, ag, sexx, act)
    await state.update_data(norm_cal=norm_cal)
    await state.update_data(min_cal=min_cal)
    diff_cal = norm_cal - min_cal
    await state.update_data(diff_cal=diff_cal)
    mess_3 = calc_3_report(norm_cal, min_cal)

    water = calculations_4(wei)
    await state.update_data(water=water)
    mess_4 = calc_4_report(water)

    protein, fat, carbohidrate = calculations_5(norm_cal)
    await state.update_data(protein=protein)
    await state.update_data(fat=fat)
    await state.update_data(carbohidrate=carbohidrate)
    mess_5 = calc_5_report(protein, fat, carbohidrate)

    # await state.update_data(state_of_use='5_подсчитано')

    date_time = datetime.now().date()

    # Записываем все данные в CSV
    data = await state.get_data()
    list_data = [data['user_id'], data['username'], data['first_name'], data['last_name'],
                 data['height'], data['weight'], data['age'], data['sex'],
                 data['imt'], data['perf_wei'], data['norm_cal'], data['min_cal'],
                 data['water'], data['protein'], date_time, data['activity'], data['fat'], data['carbohidrate']]
    await write_to_csv(list_data)

    # Записываем данные в БД
    list_values_of_DB = f"imt = {data['imt']}, perf_weight = {data['perf_wei']}, " \
                        f"protein = {data['protein']}, fat = {data['fat']}, " \
                        f"norm_cal = {data['norm_cal']}, min_cal = {data['min_cal']}, water = {data['water']}, " \
                        f"carbohidrate = {data['carbohidrate']}"

    id_in_base = get_max_id(data['user_id'])
    update_values_db(list_values_of_DB, id_in_base)