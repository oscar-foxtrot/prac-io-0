### Программная реализация метода решения классической транспортной задачи

- [Switch to English](README.md)  
- Русский (выбран)

Использование:

```python
from transportation import solve_transportation_problem
     
solve_transportation_problem(cost, supply, demand, tol=1e-12)
```

В соответствии с прототипом:

```python
def solve_transportation_problem(cost, supply, demand, tol=1e-12):
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
```

Пример:

```python
cost = np.array([
    [2, 3, 1],
    [5, 4, 8],
    [5, 6, 8]
], dtype=float)
supply = [20, 30, 25]
demand = [10, 35, 30]
