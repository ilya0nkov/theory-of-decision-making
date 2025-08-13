import tkinter as tk
from tkinter import ttk, messagebox
from LinearProgrammingProblem import LinearProgrammingProblem

class LinearProgrammingGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Линейное программирование")

        self.create_widgets()

    def create_widgets(self):
        # Таблица для коэффициентов целевой функции
        self.label_c = tk.Label(self, text="Коэффициенты целевой функции:")
        self.label_c.grid(row=0, column=0, columnspan=4, pady=5)
        self.entry_c = [tk.Entry(self) for _ in range(2)]
        for i, entry in enumerate(self.entry_c):
            entry.grid(row=1, column=i, padx=5, pady=5)

        # Таблица для коэффициентов ограничений
        self.label_A = tk.Label(self, text="Коэффициенты ограничений:")
        self.label_A.grid(row=2, column=0, columnspan=4, pady=5)
        self.entries_A = [[tk.Entry(self) for _ in range(2)] for _ in range(2)]
        for i, row in enumerate(self.entries_A):
            for j, entry in enumerate(row):
                entry.grid(row=4 + i, column=j, padx=5, pady=5)

        # Таблица для значений правой части ограничений
        self.label_b = tk.Label(self, text="Значения правой части:")
        self.label_b.grid(row=2, column=4, padx=5, pady=5)
        self.entry_b = [tk.Entry(self) for _ in range(2)]
        for i, entry in enumerate(self.entry_b):
            entry.grid(row=4 + i, column=4, padx=5, pady=5)

        # Выпадающие списки для типа ограничений
        self.label_signs = tk.Label(self, text="Типы ограничений:")
        self.label_signs.grid(row=2, column=5, padx=5, pady=5)
        self.combo_signs = [ttk.Combobox(self, values=["<=", ">=", "="]) for _ in range(2)]
        for i, combo in enumerate(self.combo_signs):
            combo.current(0)
            combo.grid(row=4 + i, column=5, padx=5, pady=5)

        # Поля для границ переменных
        self.label_bounds = tk.Label(self, text="Границы переменных:")
        self.label_bounds.grid(row=0, column=6, columnspan=2, pady=5)
        self.entries_bounds = [[tk.Entry(self) for _ in range(2)] for _ in range(2)]
        for i, row in enumerate(self.entries_bounds):
            for j, entry in enumerate(row):
                entry.grid(row=2 + i, column=6 + j, padx=5, pady=5)

        # Кнопка для добавления строк и столбцов
        self.add_row_button = tk.Button(self, text="Добавить строку", command=self.add_row)
        self.add_row_button.grid(row=20, column=0, pady=10)
        self.add_col_button = tk.Button(self, text="Добавить столбец", command=self.add_col)
        self.add_col_button.grid(row=20, column=1, pady=10)

        # Кнопка для удаления строк и столбцов
        self.del_row_button = tk.Button(self, text="Удалить строку", command=self.del_row)
        self.del_row_button.grid(row=22, column=0, pady=10)
        self.del_col_button = tk.Button(self, text="Удалить столбец", command=self.del_col)
        self.del_col_button.grid(row=22, column=1, pady=10)

        # Выпадающий список для выбора метода
        self.label_method = tk.Label(self, text="Метод:")
        self.label_method.grid(row=24, column=0, pady=5)
        self.combo_method = ttk.Combobox(self, values=["Минимизация", "Максимизация"])
        self.combo_method.current(0)
        self.combo_method.grid(row=24, column=1, pady=5)

        # Кнопка для решения задачи
        self.solve_button = tk.Button(self, text="Рассчитать", command=self.solve)
        self.solve_button.grid(row=26, column=0, columnspan=2, pady=10)

        # Метка для отображения результата
        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=27, column=0, columnspan=2, pady=5)

    def add_row(self):
        new_entries = [tk.Entry(self) for _ in range(len(self.entries_A[0]))]
        self.entries_A.append(new_entries)
        for i, entry in enumerate(new_entries):
            entry.grid(row=4 + len(self.entries_A) - 1, column=i, padx=5, pady=5)

        new_entry_b = tk.Entry(self)
        self.entry_b.append(new_entry_b)
        new_entry_b.grid(row=4 + len(self.entry_b) - 1, column=4, padx=5, pady=5)

        new_combo = ttk.Combobox(self, values=["<=", ">=", "="])
        new_combo.current(0)
        self.combo_signs.append(new_combo)
        new_combo.grid(row=4 + len(self.combo_signs) - 1, column=5, padx=5, pady=5)

    def add_col(self):
        # Добавление столбца для коэффициентов целевой функции
        new_entry_c = tk.Entry(self)
        new_entry_c.grid(row=2, column=len(self.entry_c), padx=5, pady=5)
        self.entry_c.append(new_entry_c)

        # Добавление столбца для коэффициентов ограничений
        for i, row in enumerate(self.entries_A):
            new_entry = tk.Entry(self)
            new_entry.grid(row=4 + i, column=len(row), padx=5, pady=5)
            row.append(new_entry)

        # Обновление количества строк для границ переменных
        self.update_bounds_rows()

    def del_row(self):
        if len(self.entries_A) > 1:
            for entry in self.entries_A[-1]:
                entry.grid_forget()
            self.entries_A.pop()

            self.entry_b[-1].grid_forget()
            self.entry_b.pop()

            self.combo_signs[-1].grid_forget()
            self.combo_signs.pop()

    def del_col(self):
        if len(self.entries_A[0]) > 1:
            # Удаление столбца для коэффициентов целевой функции
            self.entry_c[-1].grid_forget()
            self.entry_c.pop()

            # Удаление столбца для коэффициентов ограничений
            for row in self.entries_A:
                row[-1].grid_forget()
                row.pop()

            # Обновление количества строк для границ переменных
            self.update_bounds_rows()

    def update_bounds_rows(self):
        # Удаление всех строк в entries_bounds
        for row in self.entries_bounds:
            for entry in row:
                entry.grid_forget()
        self.entries_bounds = []

        # Добавление новых строк для границ переменных в соответствии с количеством коэффициентов целевой функции
        for i in range(len(self.entry_c)):
            new_row = [tk.Entry(self) for _ in range(2)]
            self.entries_bounds.append(new_row)
            for j, entry in enumerate(new_row):
                entry.grid(row=2 + i, column=6 + j, padx=5, pady=5)

    def solve(self):
        try:
            c = [float(entry.get()) for entry in self.entry_c]
            A = [[float(entry.get()) for entry in row] for row in self.entries_A]
            b = [float(entry.get()) for entry in self.entry_b]
            signs = [combo.get() for combo in self.combo_signs]
            bounds = [(float(row[0].get()) if row[0].get().lower() != "none" else None,
                       float(row[1].get()) if row[1].get().lower() != "none" else None) for row in self.entries_bounds]

            maximize = self.combo_method.get() == "Максимизация"

            lp_problem = LinearProgrammingProblem(c, A, b, bounds, signs=signs, maximize=maximize)
            result = lp_problem.solve()
            if result[0] is not None and result[1] is not None:
                solution = result[0]
                objective_value = result[1]
                self.result_label.config(text=f"Оптимальное решение: {solution}\nЗначение целевой функции: {objective_value}")
            else:
                self.result_label.config(text="Решение не найдено")

        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения.")

if __name__ == "__main__":
    app = LinearProgrammingGUI()
    app.mainloop()
