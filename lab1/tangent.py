import numpy as np
import matplotlib.pyplot as plt


def f(x):
    if x > 5 or x < -1e10:
        return float('inf')
    try:
        return 3 * ((5 - x) ** (3 / 4)) + 2 * x ** 2
    except OverflowError:
        return float('inf')


def df(x):
    if x > 5 or x < -1e10:
        return float('inf')
    try:
        return 4 * x - (9 / (4 * ((5 - x) ** (1 / 4))))
    except OverflowError:
        return float('inf')


def tangent_method(a, b, epsilon):
    counter = 0
    x_new = (f(b) - df(b) * b - f(a) + df(a) * a) / (df(a) - df(b))
    p0 = df(a)
    p1 = df(b)

    x_values = [a, b]
    y_values = [f(a), f(b)]

    flag = False
    while not flag:
        counter += 1

        if p1 - p0 == 0:
            break

        t1 = (f(x_new) - df(x_new) * x_new - f(a) + p0 * a) / max(p0 - df(x_new), 1e-10)
        t2 = (f(x_new) - df(x_new) * x_new - f(b) + p1 * b) / max(p1 - df(x_new), 1e-10)

        y1 = f(t1)
        y2 = f(t2)


        if isinstance(y1, complex) or isinstance(y2, complex):
            print("Комплексные значения, пропуск итерации")
            flag = True
            continue
        if np.isinf(y1) or np.isinf(y2):
            print("Чрезмерно большие значения, пропуск итерации")
            flag = True
            continue

        if y2 < y1:
            a = x_new
            x_new = t2
            p0 = df(a)
            p1 = df(x_new)
        else:
            b = x_new
            x_new = t1
            p0 = df(x_new)
            p1 = df(b)

        x_values.append(x_new)
        y_values.append(f(x_new))

        if abs(y2 - y1) < epsilon:
            flag = True
            continue

    return counter, x_new, x_values, y_values

a = 0.1
b = 2.0
epsilon = 1e-6

iterations, min_x, x_values, y_values = tangent_method(a, b, epsilon)

print("Метод касательных:")
print(f'Найденный минимум: x = {min_x}, f(x) = {f(min_x)}')
print(f'Количество итераций: {iterations}')

plt.figure(figsize=(10, 6))
plt.plot(x_values, y_values, marker='o', linestyle='-', color='blue', label='Итерации метода касательных')
plt.scatter(min_x, f(min_x), color='red', label='Минимум методом касательных', zorder=5)
plt.title('График метода касательных')
plt.xlabel('x')
plt.ylabel('Значение функции')
plt.legend()
plt.grid(True)

plt.xticks(np.arange(0, max(x_values) + 0.5, 0.5))
plt.yticks(np.arange(0, max(y_values) + 0.5, 0.5))
plt.show()
