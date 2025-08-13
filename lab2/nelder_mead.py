from math import sqrt


def func(x1, x2):
    return sqrt((x1 ** 2) + (x2 ** 2) + 1) + (x1 / 2) - (x2 / 2)


def nelder_mead(func, initial_simplex, alpha=1, gamma=2, rho=0.5, sigma=0.5, epsilon=1e-5, max_iterations=1000):
    """
    Реализация метода Нелдера-Мида для поиска минимума функции нескольких переменных.

    :param func: Целевая функция, зависящая от нескольких переменных (например, func(x1, x2))
    :param initial_simplex: Начальный симплекс в виде списка точек (список списков, например, [[x1, x2], [y1, y2], ...])
    :param alpha: Коэффициент отражения
    :param gamma: Коэффициент растяжения
    :param rho: Коэффициент сжатия
    :param sigma: Коэффициент уменьшения симплекса
    :param epsilon: Точность, для остановки алгоритма
    :param max_iterations: Максимальное количество итераций для предотвращения зацикливания
    :return: Точка минимума и значение функции в этой точке
    """
    points = initial_simplex
    iterations = 0

    while iterations < max_iterations:
        # Сортируем точки симплекса по значениям функции
        points = sorted(points, key=lambda x: func(*x))
        best, worst, second_worst = points[0], points[-1], points[-2]

        # Проверяем условие остановки
        if abs(func(*best) - func(*worst)) < epsilon:
            break

        # Вычисляем центр тяжести всех точек, кроме худшей
        centroid = [sum(x[i] for x in points[:-1]) / (len(points) - 1) for i in range(len(best))]

        # Отражение
        reflected = [centroid[i] + alpha * (centroid[i] - worst[i]) for i in range(len(best))]
        if func(*reflected) < func(*best):
            # Растяжение
            expanded = [centroid[i] + gamma * (reflected[i] - centroid[i]) for i in range(len(best))]
            if func(*expanded) < func(*reflected):
                points[-1] = expanded
            else:
                points[-1] = reflected
        else:
            # Сжатие
            if func(*reflected) < func(*second_worst):
                points[-1] = reflected
            else:
                contracted = [centroid[i] + rho * (worst[i] - centroid[i]) for i in range(len(best))]
                if func(*contracted) < func(*worst):
                    points[-1] = contracted
                else:
                    # Уменьшение симплекса
                    points = [[best[i] + sigma * (x[i] - best[i]) for i in range(len(best))] for x in points]

        iterations += 1

    # Возвращаем точку минимума и значение функции
    return best, func(*best), iterations


if __name__ == "__main__":
    # Начальный симплекс (например, треугольник в двумерном пространстве)
    initial_simplex = [[1, 2], [1.5, 1.5], [2, 1]]

    # Запуск метода Нелдера-Мида
    minimum_point, minimum_value, num_iterations = nelder_mead(func, initial_simplex)

    print("Минимальная точка:", minimum_point)
    print("Значение функции в минимальной точке:", minimum_value)
    print("Количество итераций:", num_iterations)
