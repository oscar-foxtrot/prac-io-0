import numpy as np

tol = 1e-12

def find_nwc(supply, demand):
    """
    Нахождение начального базисного допустимого решения
    методом северо-западного угла
    input:
    supply, demand --- векторы ограничений н
    спрос и предложение соответственно
    output:
    x --- начальное базисное допустимое решение,
    представленное в виде матрицы размера m x n
    basics --- номера базисных переменных
    """
    m, n = len(supply), len(demand)
    x = np.zeros((m, n))
    i = j = 0

    supply = supply.copy()
    demand = demand.copy()

    basics = set()

    while i < m and j < n:
        print(i, j, abs(supply[i]), abs(demand[j]))

        # Частичная защита от ошибок округления floating-point чисел
        if abs(supply[i]) < tol:
            supply[i] = 0
        if abs(demand[j]) < tol:
            demand[j] = 0

        print(i, j, abs(supply[i]), abs(demand[j]))

        basics.add((i, j))
        x[i, j] = min(supply[i], demand[j])

        if supply[i] < demand[j]:
            demand[j] -= x[i, j]
            i += 1
        else:
            supply[i] -= x[i, j]
            if j < n - 1:
                j += 1
            else:  # Случай, если есть нулевые ограничения
                i += 1
        print(i, j, '\n')

    return x, basics



def find_d_cyclic(basics, kl_entering, n, m):
    """
    Построение допустимого направления невозрастания функции
    путем нахождения цикла через базисные переменные и 
    вводимую переменную с использованием матричного метода,
    представленного в описании алгоритма
    (https://github.com/oscar-foxtrot/prac-io-0/tree/main/year_4_assignment_2)
    input:
    basics --- множество номеров базисных переменных
    entering --- номер вводимой переменной
    n, m --- числа, задающие размерность
    output:
    d --- допустимое направление невозрастания целевой функции
    """

    visited_sets = list()

    R_prev = {kl_entering[0]}
    C_prev = {kl_entering[1]}
    basics_visited = set()
    R = {i for i in range(m)}
    C = {i for i in range(n)}
    
    new_basics = set()
    while True:

        # строковый шаг (нечетный)
        # выбрать непосещенные базисные переменные из текущей строки
        new_basics = {(i, j) for i in R_prev for j in C - C_prev if (i, j) in basics}
        visited_sets += [new_basics]

        if any(j == kl_entering[1] for (i, j) in new_basics):
            # достигли столбца вводимой переменной => закончить шаги
            break

        # обновление множества текущих столбцов
        C_prev = {j for (i, j) in new_basics}

        # столбцовый шаг (четный)
        # выбрать непосещенные базисные переменные из текущего столбца
        new_basics = {(i, j) for j in C_prev for i in R - R_prev if (i, j) in basics}
        visited_sets += [new_basics]

        # обновление множества текущих строк
        R_prev = {i for (i, j) in new_basics}

    # нахождение цикла (обратный ход):
    current_set_number_from_the_end = 1
    current_basic_var = kl_entering
    cycle = []
    while True:
        # переходим к следующей базисной позиции по столбцу
        for i in range(m):
            if (i, current_basic_var[1]) in visited_sets[-current_set_number_from_the_end]:
                current_basic_var = (i, current_basic_var[1])
                cycle += [current_basic_var]
                break
        current_set_number_from_the_end += 1

        # переходим к следующей базисной позиции по строке
        # завершаем обратный ход, если достигнута строка вводимой переменной
        if current_basic_var[0] == kl_entering[0]:
            break
        for j in range(n):
            if (current_basic_var[0], j) in visited_sets[-current_set_number_from_the_end]:
                current_basic_var = (current_basic_var[0], j)
                cycle += [current_basic_var]
                break
        current_set_number_from_the_end += 1

    # присваивание d значений 1, -1 по циклу
    d = np.zeros((m, n))
    d[kl_entering] = 1
    sign = -1
    for (i, j) in cycle:
        d[(i,j)] = sign
        sign = -sign
    
    return d

#print(find_nwc([1/3, 3, 1/7, 0], [2, 1/7, 1 + 1/3, 0]))
#print(find_nwc([2, 6, 1, 0], [4, 1, 4, 0]))
print(find_d_cyclic({(0, 2), (0, 3), (0, 4), (1, 1), (1, 5), (2, 0), (2, 5), \
    (3, 1), (3, 2), (3, 3), (4, 4), (6, 1)}, (0, 0), n=6, m=7))