import numpy as np

M = 1 ** 3

initial_table = np.array([
    [-20 * M, -7 * M - 7, -7 * M - 6, M, M, 0, 0, 0, 0],
    [10, 5, 2, -1, 0, 0, 0, 1, 0],
    [10, 2, 5, 0, -1, 0, 0, 0, 1],
    [6, 1, 0, 0, 0, 1, 0, 0, 0],
    [5, 0, 1, 0, 0, 0, 1, 0, 0]
])


def get_resolution_row(table, resolution_col_index):
    divs = []
    for i in range(1, len(table)):
        if table[i][resolution_col_index] > 0:
            div = table[i][0] / table[i][resolution_col_index]
        else:
            div = float('inf')
        divs.append(div)
    return 1 + np.argmin(divs)


def update_table(table, resolution_row_index, resolution_col_index):
    new_table = np.zeros_like(table, dtype=float)
    new_table[resolution_row_index] = table[resolution_row_index] / table[resolution_row_index][resolution_col_index]
    for row_index in range(len(table)):
        if row_index == resolution_row_index:
            continue
        new_table[row_index] = table[row_index] - (
                table[row_index][resolution_col_index] * new_table[resolution_row_index]
        )
    return new_table


def print_table(table):
    for row in table:
        print("\t".join(f"{x:>12.3f}" for x in row))
    print()


basis_indices = []

current_table = initial_table.copy()
while np.any(current_table[0] < 0):
    res_col_index = np.argmin(current_table[0])
    try:
        res_row_index = get_resolution_row(current_table, res_col_index)
    except ValueError:
        print("Оптимальное решение недостижимо: задача не ограничена.")
        break
    basis_indices.append((res_row_index, res_col_index))
    current_table = update_table(current_table, res_row_index, res_col_index)
    print(f"Таблица после итерации {len(basis_indices)}:")
    print_table(current_table)

print(f"Оптимальное значение целевой функции F(x) = {current_table[0][0]}")
