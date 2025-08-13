import numpy as np
import matplotlib.pyplot as plt


def target_function(x):
    return 3 * ((5 - x) ** (3/4)) + 2 * x ** 2


def dichotomy_method(a, b, epsilon):
    count = 0
    while (b - a) > epsilon:
        count += 1
        mid = (a + b) / 2
        x1 = (a + mid) / 2
        x2 = (mid + b) / 2

        if target_function(x1) <= target_function(x2):
            b = mid
        else:
            a = mid

    min_x = (a + b) / 2
    min_value = target_function(min_x)
    return min_x, min_value, count


a = 0.1
b = 2.0
epsilon = 1e-6

x_values = np.linspace(a, b, 100)
y_values = [target_function(x) for x in x_values]

min_x, min_value, count = dichotomy_method(a, b, epsilon)


print("Минимум, найденный методом дихотомии:")
print("x =", min_x)
print("Значение функции =", min_value)
print("Кол-во итераций =", count)


plt.figure(figsize=(10, 6))
plt.xticks([0.5, 1, 1.5, 2, 2.5])
plt.yticks([0.5, 1, 1.5, 2, 2.5])
plt.plot(x_values, y_values, label='Целевая функция')
plt.scatter(min_x, min_value, color='red', label='Минимум методом дихотомии')
plt.title('График целевой функции и минимума методом дихотомии')
plt.xlabel('x')
plt.ylabel('Значение функции')
plt.legend()
plt.grid(True)

plt.xticks(np.arange(-1, max(x_values) + 0.5, 0.5))
plt.yticks(np.arange(8, max(y_values) + 0.5, 0.5))
plt.show()

