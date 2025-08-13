import numpy as np
import matplotlib.pyplot as plt


def hooke_jeeves(f, x_start, step_size=1, epsilon=1e-6, max_iter=1000, alpha=1):
    # мин ф
    def explore(x, step_size):
        n = len(x)
        x_new = np.copy(x)
        for i in range(n):
            x_forward = np.copy(x_new)
            x_forward[i] += step_size
            if f(x_forward) < f(x_new):
                x_new = x_forward
            else:
                x_backward = np.copy(x_new)
                x_backward[i] -= step_size
                if f(x_backward) < f(x_new):
                    x_new = x_backward
        return x_new

    # Начальные условия
    x_base = np.copy(x_start)
    iteration = 0

    # Для графиков
    func_values = [f(x_base)]
    points = [x_base.copy()]

    while iteration < max_iter:
        iteration += 1

        # Исследующий шаг
        x_new = explore(x_base, step_size)

        # Если улучшение достигнуто, делаем ускоряющий шаг
        if f(x_new) < f(x_base):
            x_sample = x_base + alpha * (x_new - x_base)
            if f(x_sample) < f(x_new):
                x_base = x_sample  # Используем ускоряющий шаг
            else:
                x_base = x_new
        else:
            # Уменьшаем шаг, если улучшения нет
            step_size *= 0.5
            if step_size < epsilon:
                break

        # запись данных для графика
        func_values.append(f(x_base))
        points.append(x_base.copy())

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    points = np.array(points)

    x1_vals = np.linspace(min(points[:, 0]) - 1, max(points[:, 0]) + 1, 100)
    x2_vals = np.linspace(min(points[:, 1]) - 1, max(points[:, 1]) + 1, 100)
    x1_grid, x2_grid = np.meshgrid(x1_vals, x2_vals)

    z_vals = np.array([func([x1, x2]) for x1, x2 in zip(np.ravel(x1_grid), np.ravel(x2_grid))])
    z_grid = z_vals.reshape(x1_grid.shape)

    ax.plot_surface(x1_grid, x2_grid, z_grid, cmap="viridis", alpha=0.7)

    x1_path, x2_path = points[:, 0], points[:, 1]
    z_path = func_values
    ax.plot3D(x1_path, x2_path, z_path, 'r-', label="Путь оптимизации")

    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_zlabel("Значение функции")
    ax.set_title("Зависимость функции от x1 и x2 с отображением пути оптимизации")
    ax.legend()

    plt.show()

    return x_base, f(x_base), iteration


if __name__ == "__main__":
    def func(x):
        x1, x2 = x[0], x[1]
        return 4 * np.sqrt((x1 ** 2) + (x2 ** 2) + 1) + (x1) - (2 *x2)

    x_start = np.array([1.0, 1.0])

    minimum_point, minimum_value, num_iterations = hooke_jeeves(func, x_start)

    print("Минимальная точка:", minimum_point)
    print("Значение функции в минимальной точке:", minimum_value)
    print("Количество итераций:", num_iterations)


# x reflected = x centr + 2(x ctntr - x max)
# x expanded = x centr + 2(x ctntr - x max)
# x contracted = x centr + 2(x ctntr - x max)
# x red = x centr + 2(x ctntr - x max)
