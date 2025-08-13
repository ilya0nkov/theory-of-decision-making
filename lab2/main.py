import numpy as np
from hooke_jeeves import hooke_jeeves
from gradient import gradient_descent


def func(x_values: list):
    x1 = x_values[0]
    x2 = x_values[1]
    return np.sqrt((x1 ** 2) + (x2 ** 2) + 1) + (x1 / 2) - (x2 / 2)


if __name__ == "__main__":
    x_start = np.array([1.0, 2.0])
    result_hooke, f_min_hooke, iter_hooke = hooke_jeeves(func, x_start)
    minimum_point, minimum_value, num_iterations = gradient_descent(func, [1, 2])

    print("Метод Хука-Джависа")
    print("Точка минимума:", result_hooke)
    print("Минимальное значение функции:", f_min_hooke)
    print(f"Количество итераций: {iter_hooke}")

    print("\nГрадиентный метод с постоянным шагом (с дроблением шага)")
    print("Точка минимума:", minimum_point)
    print("Значение функции в минимальной точке:", minimum_value)
    print("Количество итераций:", num_iterations)

    print("\nРазница результатов:", abs(f_min_hooke - minimum_value))