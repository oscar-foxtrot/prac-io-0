An implementation of a method for the solution of a classical transportation problem, which is a type of a linear programming problem.

Usage:

```python
from transportation import solve_transportation_problem     
solve_transportation_problem(cost, supply, demand, tol=1e-12)
```

According ot the prototype:

```python
def solve_transportation_problem(cost, supply, demand, tol=1e-12):
    """
    Find the solution of a transportation problem
    input:
    supply, demand --- vectors defining the supply and
    demand constraints correspondingly
    cost --- m x n matrix representing the vector defining
    the cost function <c, x> to be minimized
    tol --- tolerance parameter
    output:
    x --- transportation matrix of size m x n defining
    the solution of the transportation problem
    """
```

Example:

```python
cost = np.array([
    [2, 3, 1],
    [5, 4, 8],
    [5, 6, 8]
], dtype=float)
supply = [20, 30, 25]
demand = [10, 35, 30]

x = solve_transportation_problem(cost, supply, demand)

#print(x)
```
