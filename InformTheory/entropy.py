from math import *


def entropy(x: list, yyy:list) -> float:
    result: float = 0
    for i in range(len(x)):
        if x[i] == 0:
            continue
        result += x[i] * log2(x[i]) * yyy[i]
    return result * (-1.)


if __name__ == "__main__":
    a = 0.39745
    b = 0.17198
    c = 0.43057
    d = 0.42346
    e = 0
    f = 0.57655
    g = 0.2
    h = 0.25120
    i = 0.5488
    x = [a, b, c, d, e, f, g, h, i]

    yyy = [0.47418, 0.47418, 0.47418, 0.16868, 0.16868, 0.16868, 0.35714, 0.35714, 0.35714]
    print(entropy(x, yyy))
