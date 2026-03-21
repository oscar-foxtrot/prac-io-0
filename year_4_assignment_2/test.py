from scipy.optimize import linprog
import numpy as np

from transportation import solve_transportation_problem

def solve_via_linprog(cost, supply, demand):
    """
    Решить задачу линейного программирования
    (в частности, транспортную задачу)
    с помощью солвера HiGHS из пакета scipy.optimize.linprog
    """
    m, n = cost.shape
    c = cost.flatten()

    A_eq = []
    b_eq = []

    for i in range(m):
        row = np.zeros(m * n)
        row[i * n:(i + 1) * n] = 1
        A_eq.append(row)
        b_eq.append(supply[i])

    for j in range(n):
        col = np.zeros(m * n)
        col[j::n] = 1
        A_eq.append(col)
        b_eq.append(demand[j])

    return linprog(c, A_eq=A_eq, b_eq=b_eq, method='highs').x.reshape(m, n)


def print_res(x, cost, example_number=None):
    if example_number is None:
        print("Оптимальная матрица поставок:")
        print(x)
        print("Суммарные затраты:")
        print(np.sum(x * cost), '\n')
    else:
        print(f"Оптимальная матрица поставок (пример {example_number}):")
        print(x)
        print(f"Суммарные затраты (пример {example_number}):")
        print(np.sum(x * cost))


if __name__ == "__main__":

    tol = 1e-10

    # пример 1
    cost = np.array([
        [2, 3, 1],
        [5, 4, 8],
        [5, 6, 8]
    ], dtype=float)
    supply = [20, 30, 25]
    demand = [10, 35, 30]
    
    x_0 = solve_transportation_problem(cost, supply, demand)
    print_res(x_0, cost, example_number=1)
    x_1 = solve_via_linprog(cost, supply, demand)

    print_res(x_1, cost, example_number=1)
    assert(abs(np.sum(x_0 * cost) - np.sum(x_1 * cost)) < tol)
    try:
        assert(abs(np.allclose(x_0, x_1, tol)))
    except AssertionError:
        print("Несколько оптимальных решений")
    print('\n')



    # пример 2
    cost = np.array([
        [5, 3, 1],
        [3, 2, 4],
        [4, 1, 2]
    ], dtype=float)
    supply = [10, 20, 30]
    demand = [15, 20, 25]

    
    x_0 = solve_transportation_problem(cost, supply, demand)
    print_res(x_0, cost, example_number=2)
    x_1 = solve_via_linprog(cost, supply, demand)

    print_res(x_1, cost, example_number=2)
    assert(abs(np.sum(x_0 * cost) - np.sum(x_1 * cost)) < tol)
    try:
        assert(abs(np.allclose(x_0, x_1, tol)))
    except AssertionError:
        print("Несколько оптимальных решений")
    print('\n')


    # пример 3
    cost = np.array([
        [4, 8, 5],
        [6, 7, 3]
    ], dtype=float)

    supply = [30, 50]
    demand = [20, 40, 20]

    
    x_0 = solve_transportation_problem(cost, supply, demand)
    print_res(x_0, cost, example_number=3)
    x_1 = solve_via_linprog(cost, supply, demand)

    print_res(x_1, cost, example_number=3)
    assert(abs(np.sum(x_0 * cost) - np.sum(x_1 * cost)) < tol)
    try:
        assert(abs(np.allclose(x_0, x_1, tol)))
    except AssertionError:
        print("Несколько оптимальных решений")
    print('\n')


    # пример 4
    cost = np.array([
        [3, 1, 7, 4],
        [2, 6, 5, 9],
        [8, 3, 3, 2],
        [4, 7, 2, 5]
    ], dtype=float)

    supply = [20, 30, 25, 15]
    demand = [15, 25, 30, 20]

    x_0 = solve_transportation_problem(cost, supply, demand)
    print_res(x_0, cost, example_number=4)
    x_1 = solve_via_linprog(cost, supply, demand)

    print_res(x_1, cost, example_number=4)
    assert(abs(np.sum(x_0 * cost) - np.sum(x_1 * cost)) < tol)
    try:
        assert(abs(np.allclose(x_0, x_1, tol)))
    except AssertionError:
        print("Несколько оптимальных решений")
    print('\n')

    # пример 5
    cost = np.array([
        [8, 6, 10, 9, 7],
        [9, 12, 13, 8, 6],
        [14, 9, 16, 5, 10],
        [7, 8, 9, 12, 11],
        [10, 11, 8, 9, 12],
        [6, 5, 7, 8, 9],
    ], dtype=float)

    supply = [40, 50, 30, 60, 35, 35]
    demand = [30, 45, 60, 50, 65]

    x_0 = solve_transportation_problem(cost, supply, demand)
    print_res(x_0, cost, example_number=5)
    x_1 = solve_via_linprog(cost, supply, demand)

    print_res(x_1, cost, example_number=5)
    assert(abs(np.sum(x_0 * cost) - np.sum(x_1 * cost)) < tol)
    try:
        assert(abs(np.allclose(x_0, x_1, tol)))
    except AssertionError:
        print("Несколько оптимальных решений")
    print('\n')