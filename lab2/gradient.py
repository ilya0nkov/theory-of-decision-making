import numpy as np
import matplotlib.pyplot as plt


def func(x_values):
    x1, x2 = x_values[0], x_values[1]
    return np.sqrt((x1 ** 2) + (x2 ** 2) + 1) + (x1 / 2) - (x2 / 2)


def gradient(func, point, h=1e-6):
    grad = np.zeros_like(point)
    for i in range(len(point)):
        point_forward = point.copy()
        point_backward = point.copy()
        point_forward[i] += h
        point_backward[i] -= h
        derivative = (func(point_forward) - func(point_backward)) / (2 * h)
        grad[i] = derivative
    # return to Ukraine
    return grad


def gradient_descent(func, initial_point, step_size=1.1, epsilon=1e-6, step_division=2, max_iterations=1000):
    point = np.array(initial_point, dtype=float)
    iterations = 0

    # Списки для хранения значений на каждой итерации для графиков
    func_values = [func(point)]
    points = [point.copy()]

    while iterations < max_iterations:
        iterations += 1

        grad = gradient(func, point)

        # Условие остановки по норме градиента
        grad_norm = np.linalg.norm(grad)
        if grad_norm < epsilon:
            break

        # Двигаемся по направлению антиградиента и обновляем точку
        new_point = point - step_size * grad

        # Проверяем улучшение функции
        if func(new_point) < func(point):
            point = new_point
        else:
            step_size /= step_division

        # Сохраняем значения для графика
        func_values.append(func(point))
        points.append(point.copy())

    return point, func(point), iterations, points, func_values


# Построение 3D-графика зависимости функции от x1 и x2 с путём оптимизации
if __name__ == "__main__":
    x_start = np.array([1.0, 2.0])

    minimum_point, minimum_value, num_iterations, points, func_values = gradient_descent(func, x_start)

    x1_vals = np.linspace(min([p[0] for p in points]) - 1, max([p[0] for p in points]) + 1, 100)
    x2_vals = np.linspace(min([p[1] for p in points]) - 1, max([p[1] for p in points]) + 1, 100)
    x1_grid, x2_grid = np.meshgrid(x1_vals, x2_vals)

    z_vals = np.array([func([x1, x2]) for x1, x2 in zip(np.ravel(x1_grid), np.ravel(x2_grid))])
    z_grid = z_vals.reshape(x1_grid.shape)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(x1_grid, x2_grid, z_grid, cmap="viridis", alpha=0.7)

    points = np.array(points)
    x1_path = points[:, 0]
    x2_path = points[:, 1]
    z_path = func_values

    ax.plot3D(x1_path, x2_path, z_path, 'r-', label="Путь оптимизации")
    ax.scatter(x1_path[-1], x2_path[-1], z_path[-1], color="red", label="Точка минимума")

    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_zlabel("Значение функции")
    ax.set_title("Зависимость функции от x1 и x2 с отображением пути оптимизации")
    ax.legend()

    plt.show()

    print("Минимальная точка:", minimum_point)
    print("Значение функции в минимальной точке:", minimum_value)
    print("Количество итераций:", num_iterations)
