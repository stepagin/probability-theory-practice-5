from collections import Counter

import numpy as np
from prettytable import PrettyTable
import matplotlib.pyplot as plt


def get_frequency_matrix(s):
    """
    Возвращает таблицу частостей по выборке.
    """
    d = Counter(s)
    n = len(s)
    matrix = []
    for k, v in d.items():
        matrix.append([k, v / n])
    matrix.sort()
    return np.array(matrix)


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
    fig, axs = plt.subplots(1, 3)
    p1, p2, p3 = axs

    p1.set_title("Функция распределения")
    p1.plot(x, y, c='r')
    p1.fill_between(x, y, y2=0)
    p1.grid(True)
    p1.xaxis.set_ticks_position('bottom')
    p1.yaxis.set_ticks_position('left')

    p2.set_title("Гистограмма")
    hist = p2.hist(x, bins)

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

    print("Вариационный ряд:", sorted(numbers))
    print("Экстремальные значения:", min(numbers), "-", max(numbers))
    print("Размах выборки:", max(numbers) - min(numbers))
    print("Матожидание:", get_math_expectation(numbers))
    print("Среднеквадратичное отклонение:", np.sqrt(get_variance(numbers)))
    partsum = [frequency_matrix[0, 1]]
    for i in range(1, len(frequency_matrix)):
        partsum.append(round(partsum[i - 1] + frequency_matrix[i, 1], 2))
    table = PrettyTable(list(frequency_matrix[:, 0]))
    table.add_row(partsum)
    print("Функция распределения:")
    print(table)
    # if yes_or_no_input("Покаказать графики?"):
    #     draw_graphics(frequency_matrix[:, 0], partsum)
    draw_graphics(frequency_matrix[:, 0], partsum)

    file.close()
