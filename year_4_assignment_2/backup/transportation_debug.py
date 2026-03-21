import numpy as np

def find_nwc(supply, demand, tol=1e-12):
    """
    Нахождение начального базисного допустимого решения
    методом северо-западного угла
    input:
    supply, demand --- векторы ограничений на
    спрос и предложение соответственно
    tol --- параметр точности
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

        # частичная защита от ошибок округления floating-point чисел
        if abs(supply[i]) < tol:
            supply[i] = 0
        if abs(demand[j]) < tol:
            demand[j] = 0

        basics.add((i, j))
        x[i, j] = min(supply[i], demand[j])

        if supply[i] < demand[j]:
            demand[j] -= x[i, j]
            i += 1
        else:
            supply[i] -= x[i, j]
            if j < n - 1:
                j += 1
            else:  # случай, если есть нулевые ограничения
                i += 1

    return x, basics


def find_potentials(x, c, basics):
    """
    Вычисление потенциалов
    input:
    x --- матрица поставок размера m x n
    c --- матрица, задающая целевую функцию (m x n)
    basics --- множество номеров базисных переменных
    output:
    u, v --- векторы потенциалов
    (u --- размера m, v --- размера n)
    """
    m, n = x.shape
    u = np.full(m, np.nan)
    v = np.full(n, np.nan)
    
    # один потенциал фиксируется (принимается равным 0)
    u[0] = 0
    updated = True
    while updated:
        updated = False
        for i in range(m):
            for j in range(n):
                # для базисных переменных по мере возможности
                # решаются уравнения на потенциалы (метод распространения)
                if (i, j) in basics:
                    if not np.isnan(u[i]) and np.isnan(v[j]):
                        v[j] = c[i, j] - u[i]
                        updated = True
                    elif np.isnan(u[i]) and not np.isnan(v[j]):
                        u[i] = c[i, j] - v[j]
                        updated = True

    return u, v


def find_reduced_costs(x, c, u, v, tol=1e-12):
    """
    Вычисление значений симплекс-множителей (\\delta_{ij})
    input:
    x --- матрица поставок размера m x n
    c --- матрица, задающая целевую функцию (m x n)
    u, v --- потенциалы
    tol --- параметр точности
    output:
    delta --- матрица симплекс-множителей размера m x n
    """
    m, n = x.shape
    delta = np.zeros((m, n))

    for i in range(m):
        for j in range(n):
            reduced_cost = c[i, j] - (u[i] + v[j])
            if abs(reduced_cost) < tol:
                reduced_cost = 0
            delta[i, j] = reduced_cost

    return delta


def find_entering(delta, x):
    """
    Нахождение вводимой в базис переменной
    с минимальным индексом
    input:
    x --- матрица поставок размера m x n
    delta --- матрица симплекс-множителей размера m x n
    output:
    (i, j) или None --- номер вводимой переменной
    """

    # найти переменную, которой соответствует
    # отрицательный симплекс-множитель
    for i in range(delta.shape[0]):
        for j in range(delta.shape[1]):
            if delta[i, j] < 0:
                return (i, j)


def find_d_cyclic(basics, kl_entering, m, n):
    """
    Построение допустимого направления невозрастания функции
    путем нахождения цикла через базисные переменные и 
    вводимую переменную с использованием матричного метода,
    представленного в описании алгоритма
    (https://github.com/oscar-foxtrot/prac-io-0/tree/main/year_4_assignment_2)
    input:
    basics --- множество номеров базисных переменных
    kl_entering --- номер вводимой переменной
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


def pivot(x, d, tol=1e-12):
    """
    Найти новое базисное допустимое решение вдоль направления d,
    найти выводимую из базиса переменную с минимальным индексом
    input:
    x --- матрица поставок размера m x n
    d --- допустимое направление невозрастания целевой функции
    tol --- параметр точности
    output:
    x_star --- матрица поставок размера m x n, задающая новое
    базисное допустимое решение
    pq_leaving --- номер выводимой из базиса переменной
    """

    # максимальный шаг находится из условия theta = np.min(x[d < 0])
    # где d < 0 <=> d == -1
    
    m = x.shape[0]
    n = x.shape[1]
    theta = None
    for i in range(m):
        for j in range(n):
            if d[i, j] < 0 \
                and (theta is None or x[i, j] < theta):
                pq_leaving = (i, j)
                theta = x[i, j]  
    
    x_star = x + theta * d

    # частичная защита от ошибок округления floating-point чисел
    x_star[np.abs(x_star) < tol] = 0

    return x_star, pq_leaving


def solve_transportation_problem(cost, supply, demand, tol=1e-12, debug_mode=False):
    """
    Найти решение транспортной задачи
    input:
    supply, demand --- векторы ограничений на
    спрос и предложение соответственно
    cost --- матрица, задающая целевую функцию (m x n)
    tol --- параметр точности
    output:
    x --- матрица поставок размера m x n, задающая
    решение транспортной задачи
    """

    # найти начальное базисное допустимое решение
    # методом северо-западного угла
    x, basics = find_nwc(supply, demand, tol)
    if debug_mode:
        step = 0

    while True:

        if debug_mode:
            step += 1
            print(f"Матрица поставок, шаг {step}:\n", x)
            print(f"Номера базисных переменных, шаг {step}:\n", basics)

        # вычислить потенциалы и симплекс-множители
        u, v = find_potentials(x, cost, basics)
        delta = find_reduced_costs(x, cost, u, v, tol)

        # найти вводимую в базис переменную или завершить шаги,
        # если найденное решение оптимальное
        entering = find_entering(delta, x)
        if entering is None:
            break

        # обновить x, обновить номера базисных переменных
        d = find_d_cyclic(basics, entering, x.shape[0], x.shape[1])
        x, leaving = pivot(x, d, tol)
        basics.add(entering)
        basics -= {leaving}

    return x