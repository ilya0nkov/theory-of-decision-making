from scipy.optimize import linprog
from SimplexMethod import *

class LinearProgrammingProblem:
    count = 0

    def __init__(self, c, A, b, bounds=None, method='highs', signs=None, maximize=False):
        self.c = [-ci for ci in c] if maximize else c  # меняем знаки коэффициентов для максимизации
        self.original_c = c  # исходные коэффициенты
        self.A = A
        self.b = b
        self.bounds = bounds
        self.method = method
        self.signs = signs if signs is not None else ['<='] * len(b)
        self.solution = None
        self.objective_value = None
        self.maximize = maximize
        LinearProgrammingProblem.count += 1

    def __str__(self):
        objective = "Maximize" if self.maximize else "Minimize"
        representation = f"{objective} Z = {self.original_c} * x\n"
        representation += "Ограничения:\n"
        for i in range(len(self.A)):
            sign = self.signs[i]
            representation += f"{self.A[i]} * x {sign} {self.b[i]}\n"
        representation += f"Границы: {self.bounds}\n"
        representation += f"Метод решения: {self.method}\n"
        return representation

    def solve(self):
        A_ub, b_ub = [], []
        A_eq, b_eq = [], []

        for i, sign in enumerate(self.signs):
            if sign == '<=':
                A_ub.append(self.A[i])
                b_ub.append(self.b[i])
            elif sign == '>=':
                A_ub.append([-a for a in self.A[i]])
                b_ub.append(-self.b[i])
            elif sign == '=':
                A_eq.append(self.A[i])
                b_eq.append(self.b[i])

        simplex_method = SimplexMethod(c=self.c, A=self.A, b=self.b)
        result = simplex_method
        print()

        result = linprog(c=self.c, A_ub=A_ub or None, b_ub=b_ub or None, A_eq=A_eq or None, b_eq=b_eq or None,
                         bounds=self.bounds, method=self.method)

        if result.success:
            self.solution = result.x
            self.objective_value = -result.fun \
                if self.maximize else result.fun
        else:
            self.solution = None
            self.objective_value = None

        return self.solution, self.objective_value

    def __len__(self):
        return len(self.c)

    def __del__(self):
        LinearProgrammingProblem.count -= 1


if __name__ == "__main__":
    c = [7, 6]
    A = [
        [2, 5],
        [5, 2]
    ]
    b = [10, 10]
    signs = [">=", ">="]
    bounds = [(0, 6), (0, 5)]  # Неотрицательные переменные
    #signs = ['<=', '<=', '<=']  # Знаки ограничений
    method = 'highs'  # Указание метода решения

    # Создание экземпляра класса для задачи максимизации (№2)
    lp_problem = LinearProgrammingProblem(c, A, b, bounds, method, signs, maximize=True)

    # Вывод задачи в понятной форме
    print("Задача максимизации:")
    print(lp_problem)

    # Решение задачи минимизации
    result = lp_problem.solve()
    if result[0] is not None and result[1] is not None:
        print(f"Оптимальное решение: {result[0]}")
        print(f"Значение целевой функции: {result[1]}")
    else:
        print("Решение не найдено")
