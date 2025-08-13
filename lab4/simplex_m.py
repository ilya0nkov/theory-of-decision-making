def func(x: list, c: list):
    x1, x2 = x
    c1, c2 = c
    return c1 * x1 + c2 * x2


def set_start_table(opportunities: list[tuple], b: list, c: list,
                    eqs: list[tuple], signs: list[str]):
    rows: int = len(b) + len(opportunities) + 1  # b + y + c
    columns: int = 1 + len(opportunities) * 2 + len(b)
    table = [[0 for _ in range(columns)] for _ in range(rows)]

    coefs = [1 for _ in range(len(signs) * 2)]
    for item in range(len(signs)):
        if signs[item].__eq__(">="):
            coefs[item] = -1

    counter_for_matrix = 0
    for col in range(columns):
        for row in range(rows):
            if col == 0:  # b
                if row < len(b):
                    table[row][col] = b[row]
                elif row < len(opportunities) * 2:
                    table[row][col] = opportunities[0][1]

            elif col <= len(b):  # x1 x2
                if row < len(b):
                    table[row][col] = eqs[row][col - 1]
                elif row < len(opportunities) * 2:
                    if row == col + len(b) - 1:
                        table[row][col] = 1
                    else:
                        table[row][col] = 0
                else:
                    table[row][col] = -1 * c[col - 1]

            elif row == counter_for_matrix and col == 1 + len(b) + counter_for_matrix:
                table[row][col] = coefs[counter_for_matrix]
                counter_for_matrix += 1
            else:
                table[row][col] = 0
    print("start table:")
    for row in table:
        print("\t".join(f"{x:>6.3f}" for x in row))
    print()
    return table, columns, rows


def run_simplex(opportunities: list[tuple], b_values: list, c_values: list,
                start_equations: list[tuple], signs: list[str]):
    table, columns, rows = set_start_table(opportunities=opportunities,
                            b=b_values, c=c_values, eqs=start_equations,
                            signs=signs)

    new_table = [row.copy() for row in table]
    x_indexes = [i for i in range(1, len(b_values)+1)]

    while any(x < 0 for x in table[-1][1:]):
        #[i] < 0 for i in x_indexes):
        new_table = [row.copy() for row in new_table]
        res_col, res_row, res_elem = get_resolutions(table=new_table)

        edited_row = []
        for item in range(len(new_table[0])):
            new_table[res_row][item] /= res_elem
            edited_row.append(new_table[res_row][item])

        division_indexes = []
        for row in range(rows):
            value = get_diff_coefficient(new_table[row][res_col], edited_row[res_col])
            division_indexes.append(value)
            if row == res_row:
                continue
            for col in range(columns):
                if new_table[row][res_col] < 0 and row == rows:
                    new_table[row][col] -= division_indexes[row][0] * division_indexes[row][1] * edited_row[col]
                new_table[row][col] -= division_indexes[row][0] * division_indexes[row][1] * edited_row[col] * -1

        print("new table:")
        for row in new_table:
            print("\t".join(f"{x:>6.3f}" for x in row))
        print()
    x_values = [new_table[-1][i] for i in x_indexes]
    print(x_values)
    return x_values


def get_diff_coefficient(current_value: float, point_value: float) -> list:
    indexes = [-1] * 2
    if current_value - point_value < 0:
        indexes[1] = 1
    try:
        indexes[0] = current_value / point_value
    except ZeroDivisionError:
        print("Zero Division Error")
    return indexes


def get_resolutions(table: list[list]) -> tuple[int, int, float]:
    c_values = table[-1]
    resolution_col_value = min(c_values[1:])
    resolution_col = c_values.index(resolution_col_value)
    print(resolution_col, "res col")
    b_col = [row[0] for row in table[:-1]]
    b_x_values = [b_col[row] / table[row][resolution_col] if table[row][resolution_col] > 0 else float('inf') for row in range(len(b_col))]

    resolution_row_value = min(b_x_values)
    resolution_row = b_x_values.index(resolution_row_value)
    resolution_elem = table[resolution_row][resolution_col]

    print(resolution_col, resolution_row, resolution_elem)
    return resolution_col, resolution_row, resolution_elem

'''
def get_resolutions(table: list[list]) -> tuple[int, int, float]:
    rows = 0
    for col in range(1):
        for row in range(len(table)):
            rows += 1

    c_values = table[-1]

    resolution_col_value = min(c_values)
    resolution_col = c_values.index(resolution_col_value)
    base_value = max(table[0]) + 1

    b_col = [0 for _ in range(rows - 1)]
    for row in range(rows - 1):
        b_col[row] = table[row][0]

    b_x_values = [0 for _ in range(rows - 1)]
    for row in range(rows - 1):
        if table[row][resolution_col] != 0:
            b_x_values[row] = b_col[row] / table[row][resolution_col]
        else:
            b_x_values[row] = base_value
    print(b_x_values)
    resolution_row_value = min(b_x_values)
    resolution_row = b_x_values.index(resolution_row_value)
    resolution_elem = table[resolution_row][resolution_col]
    print(resolution_col, resolution_row, resolution_elem)
    return resolution_col, resolution_row, resolution_elem
'''

if __name__ == "__main__":
    opportunities = [(0, 6), (0, 5)]
    b_values = [10, 10]
    c_values = [7, 6]
    start_equations = [(2, 5), (5, 2)]
    signs = [">=", ">="]

    x_values = run_simplex(opportunities=opportunities,
                b_values=b_values, c_values=c_values,
                start_equations=start_equations,
                signs=signs)
    print("answer: ", func(x=x_values, c=c_values))
