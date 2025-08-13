import math
from decimal import Decimal, getcontext


def entropy(massiv):
    sum = 0
    for key, value in massiv.items():
        sum -= value * math.log2(value)

    return sum


def float_to_binary(num, precision=10):
    """Перевод вещественного числа в двоичную систему с заданной точностью"""
    if num < 0:
        sign = "-"
        num = abs(num)
    else:
        sign = ""

    # Целая часть
    integer_part = int(num)
    fractional_part = num - integer_part

    # Переводим целую часть в двоичный формат
    integer_binary = bin(integer_part).replace("0b", "")

    # Переводим дробную часть
    fractional_binary = []
    while fractional_part and len(fractional_binary) < precision:
        fractional_part *= 2
        bit = int(fractional_part)
        fractional_binary.append(str(bit))
        fractional_part -= bit

    # Формируем результат
    return f"{sign}{integer_binary}." + "".join(fractional_binary)


def precise_binary(num, precision=10):
    getcontext().prec = precision + 2  # Устанавливаем точность
    dec_num = Decimal(num)
    return float_to_binary(float(dec_num), precision=precision)


def main(massiv):
    flag = int(input("1 - Шеннон, 2 - Гилберт мура\n"))
    flag_shen = False
    flag_gilbertmyr = False

    if flag == 1:
        flag_shen = True
        flag_gilbertmyr = False
    elif flag == 2:
        flag_shen = False
        flag_gilbertmyr = True

    evaluate(massiv, sovmestn=False, Shennon=flag_shen, Gilbert_myra=flag_gilbertmyr)
    evaluate(massiv, sovmestn=True, Shennon=flag_shen, Gilbert_myra=flag_gilbertmyr)


def evaluate(massiv, sovmestn=False, Shennon=False, Gilbert_myra=False):
    Pm = {}
    if sovmestn:
        for i in range(len(massiv)):
            for j in range(len(massiv)):
                Pm[str(i + 1) + str(j + 1)] = massiv[i] * massiv[j]
    else:
        for i in range(len(massiv)):
            Pm[str(i + 1)] = massiv[i]

    reverse = False
    if Shennon:
        reverse = True
    sort_Pm = dict(sorted(Pm.items(), key=lambda item: item[1], reverse=reverse))

    Qm = {}
    sum_qm = 0
    for key, value in sort_Pm.items():
        Qm[key] = sum_qm
        sum_qm += value

    Cm = {}

    Sigma = {}
    for key, value in Qm.items():

        if Gilbert_myra:
            Sigma[key] = sort_Pm[key] / 2 + value
        else:
            Cm[key] = precise_binary(value)

    if Gilbert_myra:
        for key, value in Sigma.items():
            Cm[key] = precise_binary(value)

    L = 0
    H = entropy(sort_Pm)
    for key, value in sort_Pm.items():
        if Gilbert_myra:
            L += value * (int(-math.log2(value / 2)) + 1)
            print(f"{key} | {Pm[key]:.4f} | {Qm[key]:.5f} | {Sigma[key]:.5f} | {Cm[key]}")
        else:
            L += value * (int(-math.log2(value)) + 1)
            print(f"{key} | {Pm[key]:.4f} | {Qm[key]:.5f} | {float(Cm[key]):.6f}")

    print(f"H = {H}")
    print(f"L = {L}")
    print(f"R = {H / L}\n")


if __name__ == "__main__":
    massiv_data = [0.145, 0.231, 0.269, 0.355]
    # massiv_data = [0.292, 0.125, 0.375, 0.208]
    main(massiv_data)