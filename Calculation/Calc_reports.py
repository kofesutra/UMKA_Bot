def calc_1_report(result):
    emo = '🔵'
    res_comment = ""
    if result < 16:
        res_comment = "выраженный дефицит массы тела (менее 16)"
        emo = '🔴'
    elif 16 <= result < 18.5:
        res_comment = "недостаточная масса тела (от 16 до 18,4)"
        emo = '🟠'
    elif 18.5 <= result < 25:
        res_comment = "нормальная масса тела (от 18,5 до 24,9)"
        emo = '🟢'
    elif 25 <= result < 30:
        res_comment = "избыточная масса тела (предожирение) (от 25 до 29,9)"
        emo = '🟠'
    elif 30 <= result < 35:
        res_comment = "ожирение I степени (от 30 до 34,9)"
        emo = '🟠'
    elif 35 <= result < 40:
        res_comment = "ожирение II степени (от 35 до 39,9)"
        emo = '🔴'
    elif 40 <= result:
        res_comment = "ожирение III степени (более 40)"
        emo = '🔴'

    # return emo + " Твой индекс массы тела " + str(result) + "\nОн находится в диапазоне: " + str(res_comment)
    return emo + " Ваш индекс массы тела " + str(result)


def calc_2_report(result):
    report = "🟢 Идеальная масса по методу Devine " + str(result) + " кг"
    return report


def calc_3_report(result_1, result_2):
    report = "🟣 Дневная норма калорий " + str(result_1) + " ккал\n❗️ Ваш основной обмен " + str(
        result_2) + " ккал"
    return report


def calc_4_report(result):
    report = "🔵 Дневная норма воды " + str(result) + " л"
    return report


def calc_5_report(result_1, result_2, result_3):
    report = f"🟠 Дневная норма белков {str(result_1)} г\n\n🟡 Дневная норма жиров {str(result_2)} г\n\n🟢 Дневная норма углеводов {str(result_3)} г"
    return report
