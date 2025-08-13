import numpy as np
import matplotlib.pyplot as plt


# Исходная нелинейная функция
def f(x):
    return 3 * ((5 - x) ** (3 / 4)) + 2 * x ** 2


# Производная функции
def df(x):
    return 4 * x - (9 / (4 * ((5 - x) ** (1 / 4))))


# Метод касательных
def tangent_method(a, b, epsilon):
    counter = 0
    x_new = (a + b) / 2  # Начальное приближение
    x_values = [x_new]
    y_values = [f(x_new)]

    while abs(df(x_new)) > epsilon:  # Условие выхода
        counter += 1

        x_new = x_new - f(x_new) / df(x_new)  # Итерация метода касательных

        x_values.append(x_new)
        y_values.append(f(x_new))

    return counter, x_new, x_values, y_values


# Метод ломанных
def broken_line_method(a, b, epsilon):
    counter = 0
    x_values = [a, b]
    y_values = [f(a), f(b)]

    while abs(b - a) > epsilon:  # Условие выхода
        counter += 1

        # Точки внутри интервала (метод деления на 3)
        mid1 = a + (b - a) / 3
        mid2 = b - (b - a) / 3

        # Значения функции в этих точках
        f_mid1 = f(mid1)
        f_mid2 = f(mid2)

        x_values.extend([mid1, mid2])
        y_values.extend([f_mid1, f_mid2])

        # Сужаем интервал
        if f_mid1 < f_mid2:
            b = mid2
        else:
            a = mid1

    min_x = (a + b) / 2  # Минимум между новыми границами
    return counter, min_x, x_values, y_values


# Задаем начальные параметры
a = 0.1
b = 2.0
epsilon = 1e-6

# Вызываем метод касательных
iterations_tangent, min_x_tangent, x_values_tangent, y_values_tangent = tangent_method(a, b, epsilon)

# Вызываем метод ломанных
iterations_broken, min_x_broken, x_values_broken, y_values_broken = broken_line_method(a, b, epsilon)

# Вывод результатов
print("Метод касательных:")
print(f'Найденный минимум (касающихся): x = {min_x_tangent}, f(x) = {f(min_x_tangent)}')
print(f'Количество итераций (касающихся): {iterations_tangent}')

print("\nМетод ломанных:")
print(f'Найденный минимум (ломанных): x = {min_x_broken}, f(x) = {f(min_x_broken)}')
print(f'Количество итераций (ломанных): {iterations_broken}')

# Построение графика
plt.figure(figsize=(12, 6))

# График метода касательных
plt.subplot(1, 2, 1)
plt.plot(x_values_tangent, y_values_tangent, marker='o', linestyle='-', color='blue', label='Метод касательных')
plt.scatter(min_x_tangent, f(min_x_tangent), color='red', label='Минимум', zorder=5)
plt.title('График метода касательных')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)

# График метода ломанных
plt.subplot(1, 2, 2)
plt.plot(x_values_broken, y_values_broken, marker='o', linestyle='-', color='green', label='Метод ломанных')
plt.scatter(min_x_broken, f(min_x_broken), color='red', label='Минимум', zorder=5)
plt.title('График метода ломанных')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
