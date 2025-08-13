from math import sqrt


def func(x1, x2):
    # return sqrt((x1 ** 2) + (x2 ** 2) + 1) + (x1 / 2) - (x2 / 2)
    return

def explore(func, base_point, step):
    """
    Исследует окрестность точки base_point с заданным шагом step.

    :param func: Целевая функция, зависящая от нескольких переменных
    :param base_point: Текущая точка, от которой ведётся исследование
    :param step: Размер шага для изменения координат
    :return: Новая точка с улучшенным значением функции или та же точка, если улучшения нет
    """
    new_point = base_point[:]
    for i in range(len(base_point)):
        new_point[i] += step
        if func(*new_point) < func(*base_point):
            base_point = new_point[:]
        else:
            new_point[i] -= 2 * step
            if func(*new_point) < func(*base_point):
                base_point = new_point[:]
            else:
                new_point[i] += step
    return base_point


def hooke_jeeves(func, initial_point, step_size=0.5, epsilon=1e-5, alpha=2, max_iterations=1000000):
    """
    Реализация метода Хука-Дживса для поиска минимума функции нескольких переменных.

    :param func: Целевая функция, зависящая от нескольких переменных (например, func(x1, x2))
    :param initial_point: Начальная точка поиска в виде списка [x1, x2, ...]
    :param step_size: Начальный шаг поиска
    :param epsilon: Точность поиска
    :param alpha: Коэффициент увеличения шага при успехе поиска
    :param max_iterations: Максимальное количество итераций для предотвращения зацикливания
    :return: Координаты точки минимума, значение функции в этой точке, количество итераций
    """
    base_point = initial_point[:]
    best_point = initial_point[:]
    iterations = 0  # Счётчик итераций

    while step_size > epsilon and iterations < max_iterations:
        iterations += 1

        # Этап исследования
        new_point = explore(func, base_point, step_size)

        # Проверяем улучшение
        if func(*new_point) >= func(*base_point):
            step_size /= alpha  # Уменьшаем шаг, если улучшений нет
        else:
            # Этап поиска по направлению
            while True:
                trial_point = [2 * new - old for new, old in zip(new_point, base_point)]

                if func(*trial_point) < func(*new_point):
                    base_point = new_point
                    new_point = trial_point
                else:
                    break

            best_point = new_point

    # Проверка, достигли ли максимального числа итераций
    if iterations >= max_iterations:
        print("Предупреждение: Достигнуто максимальное количество итераций.")

    return best_point, func(*best_point), iterations


if __name__ == "__main__":
    initial_point = [1, 2]

    # Запуск метода Хука-Дживса
    minimum_point, minimum_value, num_iterations = hooke_jeeves(func, initial_point)

    print("Минимальная точка:", minimum_point)
    print("Значение функции в минимальной точке:", minimum_value)
    print("Количество итераций:", num_iterations)
