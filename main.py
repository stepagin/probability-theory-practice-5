import sys
from collections import Counter

import numpy as np
from prettytable import PrettyTable
import matplotlib.pyplot as plt


def get_variance_matrix(s):
    """
    Возвращает таблицу частостей по выборке.
    """
    d = Counter(s)
    n = len(s)
    matrix = []
    for k, v in d.items():
        matrix.append([k, v])
    matrix.sort()
    return np.array(matrix)


def get_frequency_matrix(s):
    """
    Возвращает таблицу частостей по выборке.
    """
    fm = get_variance_matrix(s)
    for i in range(len(fm)):
        fm[i][1] /= n
    return fm


def get_math_expectation(numbers):
    """
    Возвращает матожидание по выборке.
    """
    frequency_matrix = get_frequency_matrix(numbers)
    s = 0
    for i in frequency_matrix:
        s += i[0] * i[1]
    return s


def get_variance(numbers):
    """
    Возвращает дисперсию по выборке.
    """
    fx = get_frequency_matrix(numbers)
    mx = get_math_expectation(numbers)
    mx2 = 0
    for i in fx:
        mx2 += i[0] ** 2 * i[1]
    return mx2 - mx ** 2


def empirical_distribution_function(x, freq_matrix):
    """
    Возвращает эмпирическую (статическую) функцию распределения в точке x по таблице частостей.
    """
    result = 0
    for i in freq_matrix:
        if i[0] < x:
            result += i[0]
        else:
            break
    return result


def yes_or_no_input(message=""):
    """
    Задать вопрос пользователю, ответ на который может быть либо "Да", либо "Нет".
    Возвращает True или False.
    """
    message = message + " [y/n]: "
    buf = '0'
    while buf[0].lower() not in ['y', 'n', 'д', 'н']:
        buf = input(message)
    return buf in ['y', 'д']


def draw_graphics(x, y):
    """
    Рисует графики по точкам.
    Принимает координаты точек в виде массивов по осям абсцисс и ординат.
    """
    bins = 1 + int(np.ceil(np.log2(len(x))))
    fig, p1 = plt.subplots(1, 1)
    p1.set_title("Функция распределения")
    p1.step(([min(x) - 0.3] + list(x) + [max(x) + 0.3]), ([0] + y + [1]), c='r', where="post")
    p1.grid(True)
    p1.xaxis.set_ticks_position('bottom')
    p1.yaxis.set_ticks_position('left')
    plt.show()

    fig, p2 = plt.subplots(1, 1)
    p2.set_title("Гистограмма")
    p2.grid(True)
    hist = p2.hist(x, bins)
    plt.show()

    fig, p3 = plt.subplots(1, 1)
    bars_x, bars_y = hist[1][1:], hist[0]
    p3.set_title("Полигон приведенных частот\nгруппированной выборки")
    p3.plot(bars_x, bars_y, marker='.')
    p3.grid(True)

    plt.show()


if __name__ == '__main__':
    filename = "input.txt"
    file = open(filename, "r")
    n = int(file.readline())
    numbers = [float(t) for t in file.readline().split()]
    if n != len(numbers):
        n = min(n, len(numbers))
        numbers = numbers[:n]

    frequency_matrix = get_frequency_matrix(numbers)
    variance_matrix = get_variance_matrix(numbers)

    print("Вариационный ряд:", sorted(numbers))

    print("Экстремальные значения:", min(numbers), "-", max(numbers))
    print("Размах выборки:", max(numbers) - min(numbers))
    print("Матожидание:", round(get_math_expectation(numbers), 5))
    D = get_variance(numbers)
    print("Дисперсия:", round(D, 5))
    print("Исправленная дисперсия:", round(n * D / (n - 1), 5))
    print("Среднеквадратичное отклонение:", round(np.sqrt(D), 5))
    print("Исправленное среднеквадратичное отклонение:", round(np.sqrt(n * D / (n - 1)), 5))

    partsum = [frequency_matrix[0, 1]]
    for i in range(1, len(frequency_matrix)):
        partsum.append(round(partsum[i - 1] + frequency_matrix[i, 1], 2))
    table = PrettyTable(list(frequency_matrix[:, 0]))
    table.add_row(partsum)
    print("Функция распределения:")
    print(table)

    print("F:")
    print(f"Для x < {frequency_matrix[0][0]}: 0")
    for i in range(0, len(partsum) - 1):
        print(f"Для {frequency_matrix[i][0]} <= x < {frequency_matrix[i + 1][0]}: {partsum[i]}")
    print(f"Для {frequency_matrix[-1][0]} < x: {float(1)}")
    draw_graphics(frequency_matrix[:, 0], partsum)

    file.close()
