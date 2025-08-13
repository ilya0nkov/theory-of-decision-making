import numpy as np

num_u = 3
num_v = 4
a = [30, 50, 20]
b = [15, 15, 40, 30]

matrix = np.array([
    [1, 8, 2, 3],
    [4, 7, 5, 1],
    [5, 3, 4, 4]
], dtype=float)

transport_plan = np.zeros((num_u, num_v))  # Матрица текущего транспортного плана


def build_optimal_initial_table():
    global a, b, transport_plan, matrix
    remaining_supplies = a[:]  # Оставшиеся запасы
    remaining_demands = b[:]  # Оставшиеся заказы
    covered_cells = set()  # использованные ячейки

    while sum(remaining_supplies) > 0 and sum(remaining_demands) > 0:
        min_cost = float('inf')
        min_supplier, min_consumer = -1, -1
        for supplier in range(num_u):
            for consumer in range(num_v):
                if (supplier, consumer) not in covered_cells and matrix[supplier, consumer] < min_cost:
                    min_cost = matrix[supplier, consumer]
                    min_supplier, min_consumer = supplier, consumer

        supplier, consumer = min_supplier, min_consumer
        volume_supply = min(remaining_supplies[supplier], remaining_demands[consumer])
        transport_plan[supplier, consumer] = volume_supply
        remaining_supplies[supplier] -= volume_supply
        remaining_demands[consumer] -= volume_supply
        covered_cells.add((supplier, consumer))

        if remaining_supplies[supplier] == 0:
            for col in range(num_v):
                covered_cells.add((supplier, col))
        if remaining_demands[consumer] == 0:
            for row in range(num_u):
                covered_cells.add((row, consumer))


def calculate_cost():
    total_cost = np.sum(transport_plan * matrix)  # Сумма произведений тарифов и объемов поставок
    print(f"Начальное распределение транспортировки (план):\n{transport_plan}")
    print(f"Общая стоимость транспортировки: {total_cost:.2f}")
    return total_cost


build_optimal_initial_table()
calculate_cost()
print("Конечное распределение транспортировки (план):")
print(transport_plan)
