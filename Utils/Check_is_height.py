def check_height(dig):
    dig_here = float(dig)
    if 250 > dig_here > 100:
        return 1
    else:
        return 0


def check_weight(dig):
    dig_here = float(dig)
    if 200 > dig_here > 20:
        return 1
    else:
        return 0


def check_age(dig):
    dig_here = float(dig)
    if 120 > dig_here > 10:
        return 1
    else:
        return 0
