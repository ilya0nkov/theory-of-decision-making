import numpy as np


class SimplexMethod:
    def __init__(self, c, A, b, maximize=True):
        """
        Инициализация симплекс-метода.
        :param c: Коэффициенты целевой функции (1D массив).
        :param A: Коэффициенты ограничений (2D массив).
        :param b: Правая часть ограничений (1D массив).
        :param maximize: True для задачи на максимум, False для минимума.
        """
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.maximize = maximize

        if not maximize:
            self.c = -self.c  # Для задачи минимизации инвертируем целевую функцию

        # Матрица для симплекс-таблицы
        self.num_constraints, self.num_variables = self.A.shape
        self.tableau = None
        self.basic_vars = None
        self.init_tableau()

    def preprocess_constraints(self, signs):
        """
        Обработка ограничений с разными знаками (<=, >=, =).
        :param signs: Список знаков ограничений ("<=", ">=", "=").
        """
        for i, sign in enumerate(signs):
            if sign == ">=":
                # Для >= инвертируем знак ограничения
                self.A[i, :] *= -1
                self.b[i] *= -1
            elif sign == "=":
                # Для = добавляем два ограничения: <= и >=
                self.A = np.vstack([self.A, -self.A[i, :]])
                self.b = np.hstack([self.b, -self.b[i]])

    def init_tableau(self):
        """
        Создание начальной симплекс-таблицы.
        """
        # Добавляем базисные переменные (единичная матрица)
        identity = np.eye(self.num_constraints)
        self.tableau = np.hstack([self.A, identity, self.b.reshape(-1, 1)])

        # Создаем строку целевой функции
        z_row = np.hstack([-self.c, np.zeros(self.num_constraints + 1)])

        # Полная таблица
        self.tableau = np.vstack([self.tableau, z_row])

        # Начальные базисные переменные
        self.basic_vars = list(range(self.num_variables, self.num_variables + self.num_constraints))

    def find_pivot(self):
        """
        Нахождение разрешающего столбца и строки.
        :return: (pivot_row, pivot_col)
        """
        # Разрешающий столбец (столбец с минимальным значением в строке Z)
        pivot_col = np.argmin(self.tableau[-1, :-1])
        if self.tableau[-1, pivot_col] >= 0:
            return None, None  # Оптимальное решение найдено

        # Разрешающая строка (по правилу минимального отношения)
        ratios = []
        for i in range(self.num_constraints):
            if self.tableau[i, pivot_col] > 0:
                ratios.append(self.tableau[i, -1] / self.tableau[i, pivot_col])
            else:
                ratios.append(np.inf)

        pivot_row = np.argmin(ratios)
        if ratios[pivot_row] == np.inf:
            raise ValueError("Задача не имеет решения (неограниченная функция)")

        return pivot_row, pivot_col

    def pivot(self, row, col):
        """
        Выполнение шага (поворота) симплекс-метода.
        :param row: Номер разрешающей строки.
        :param col: Номер разрешающего столбца.
        """
        # Обновляем разрешающую строку
        self.tableau[row, :] /= self.tableau[row, col]

        # Обновляем остальные строки
        for i in range(self.tableau.shape[0]):
            if i != row:
                self.tableau[i, :] -= self.tableau[i, col] * self.tableau[row, :]

        # Обновляем базисные переменные
        self.basic_vars[row] = col

    def solve(self):
        """
        Решение задачи симплекс-методом.
        :return: Оптимальное решение и значение целевой функции.
        """
        while True:
            # Находим разрешающий элемент
            pivot_row, pivot_col = self.find_pivot()
            if pivot_row is None:  # Оптимальное решение найдено
                break
            self.pivot(pivot_row, pivot_col)

        # Извлекаем оптимальное решение
        solution = np.zeros(self.num_variables)
        for i, var in enumerate(self.basic_vars):
            if var < self.num_variables:
                solution[var] = self.tableau[i, -1]

        # Оптимальное значение целевой функции
        optimal_value = self.tableau[-1, -1]
        if not self.maximize:
            optimal_value = -optimal_value  # Для задачи минимизации возвращаем оригинальный знак
        return solution, optimal_value

    @staticmethod
    def from_user_input():
        """
        Создание задачи линейного программирования на основе пользовательского ввода.
        """
        print("Введите количество переменных:")
        num_variables = int(input())

        print("Введите количество ограничений:")
        num_constraints = int(input())

        print("Введите коэффициенты целевой функции через пробел:")
        c = list(map(float, input().split()))

        print("Введите матрицу ограничений (по строкам, через пробел):")
        A = []
        for _ in range(num_constraints):
            A.append(list(map(float, input().split())))

        print("Введите правую часть ограничений (вектор b):")
        b = list(map(float, input().split()))

        print("Введите знаки ограничений (<=, >=, =) через пробел:")
        signs = input().split()

        print("Максимизация (1) или минимизация (0)? Введите 1 или 0:")
        maximize = bool(int(input()))

        simplex = SimplexMethod(c, A, b, maximize)
        simplex.preprocess_constraints(signs)
        return simplex


# Пример использования
if __name__ == "__main__":
    c = [0, 0]
    A = [
        [3, 2],
        [2, -3],
        [1, -1],
        [4, 7]
    ]
    b = [6, -6, 4, 28]
    signs = [">=", ">=", "<=", "<="]
    simplex = SimplexMethod(c, A, b, maximize=True)
    simplex.preprocess_constraints(signs)

    #simplex = SimplexMethod(c, A, b, maximize=False)
    solution, optimal_value = simplex.solve()

    print("Оптимальное решение (x):", solution)
    print("Оптимальное значение (Z):", optimal_value)
