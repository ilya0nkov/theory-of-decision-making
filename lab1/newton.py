import math
import numpy as np
import matplotlib.pyplot as plt


def target_function(x):
    return 3 * ((5 - x) ** (3 / 4)) + 2 * x ** 2


def gradient(x):
    return - (9 / (4 * (5 - x) ** (1 / 4))) + 4 * x


def hessian(x):
    return 9 / (16 * (5 - x) ** (5 / 4)) + 4


def newton_method(initial_guess, epsilon):
    x0 = initial_guess
    count = 0

    flag = False
    while not flag:
        count += 1
        gradient_value = gradient(x0)
        hessian_value = hessian(x0)

        if hessian_value == 0:
            flag = True
            continue

        x1 = x0 - gradient_value / hessian_value

        if abs(x1 - x0) < epsilon:
            flag = True
            continue

        x0 = x1

    min_x = x0
    min_value = target_function(min_x)
    return min_x, min_value, count


initial_guess_newton = 4.9
epsilon_newton = 1e-6

x_values = np.linspace(0.1, 2.0, 100)
y_values = [target_function(x) for x in x_values]

min_x_newton, min_value_newton, count = newton_method(initial_guess_newton, epsilon_newton)

print("Минимум, найденный методом Ньютона:")
print("x =", min_x_newton)
print("Значение функции =", min_value_newton)
print("Кол-во итераций =", count)

plt.figure(figsize=(10, 6))
plt.plot(x_values, y_values, label='Целевая функция')
plt.scatter(min_x_newton, min_value_newton, color='red', label='Минимум методом Ньютона')
plt.title('График целевой функции и минимума методом Ньютона')
plt.xlabel('x')
plt.ylabel('Значение функции')
plt.legend()
plt.grid(True)

plt.xticks(np.arange(-1, max(x_values) + 0.5, 0.5))
plt.yticks(np.arange(8, max(y_values) + 0.5, 0.5))
plt.show()


