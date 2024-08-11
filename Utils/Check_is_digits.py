def check_digits(dig_input):
    dig = dig_input
    if dig.isdigit():  # Если целое число
        return dig
    elif dig.replace('.', '', 1).isdigit():  # Если дробное: убираем точку и проверяем на целое число
        return dig
    elif dig.replace(',', '.', 1).replace('.', '', 1).isdigit():  # Если с запятой, то меняем её на точку и проверяем
        dig = dig.replace(',', '.', 1)
        return dig
    else:
        return 1639572
