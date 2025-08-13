import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return 3 * ((5 - x) ** (3 / 4)) + 2 * x ** 2


def df(x):
    return 4 * x - (9 / (4 * ((5 - x) ** (1 / 4))))


def secant_method(f, df, x0, x1, max_iter=1000):
    iteration = 0

    for _ in range(max_iter):
        iteration += 1
        print("iter =", iteration)
        f_prime_x0 = df(x0)
        print(x0, " производная ", f_prime_x0)
        f_prime_x1 = df(x1)
        print(x1, " производная ", f_prime_x1)
        print("abs = ", abs(f_prime_x1 - f_prime_x0))
        if abs(f_prime_x1 - f_prime_x0) < epsilon:
            print("Малая разница производных, возможно деление на ноль.")
            return x1, f(x1), iteration

        x2 = x1 - f_prime_x1 * (x1 - x0) / (f_prime_x1 - f_prime_x0)

        if abs(x2 - x1) < epsilon:
            return x2, f(x2), iteration

        x0, x1 = x1, x2

    print(f"Достигнуто максимальное количество итераций: {max_iter}")
    return x1, f(x1), iteration


x0 = -1
x1 = 3
epsilon = 1e-10


x_secant, f_secant, iter_secant = secant_method(f, df, x0, x1)
print("кол-во итераций:", iter_secant)

x_vals = np.linspace(x0, x1, 4000)
y_vals = [f(x) for x in x_vals]
plt.plot(x_vals, y_vals, label="f(x)", color="blue")

plt.scatter(x_secant, f_secant, color="green", label=f"Секущие (x={x_secant:.6f}, f(x)={f_secant:.6f})")

plt.title("График методом секущих")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)

plt.xticks(np.arange(-1, x1 + 0.5, 0.5))
plt.yticks(np.arange(8, max(y_vals) + 0.5, 0.5))

plt.show()