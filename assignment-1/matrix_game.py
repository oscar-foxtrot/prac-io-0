from typing import Tuple
import numpy as np
import scipy as sp
import copy

# Payoff matrix is represented by np.ndarray

def nash_equilibrium(payoff_matrix: np.ndarray) -> \
        Tuple[float, np.ndarray, np.ndarray]:    
    """
    Solves a matrix game with the given "payoff_matrix" matrix
    
    Parameters:
    - payoff_matrix (np.ndarray): The matrix representing the game
    
    Returns:
    Tuple[float, np.ndarray, np.ndarray]: 
    A tuple containing the game value, the 1st player's strategy,
    and the 2nd player's strategy.
    """

    '''
    When solving the problem using the simplex method, we will use a function 
    from the scipy library. You can find more details about it 
    here: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html#scipy.optimize.linprog
    The function has the following signature:
        scipy.optimize.linprog(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, 
                               bounds=None, method='highs', callback=None, 
                               options=None, x0=None, integrality=None)
    Where:
        - `c`: Coefficients of the objective function to be minimized.
        - `A_ub`: Matrix defining the coefficients of the linear inequality 
          constraints, each row representing one constraint.
        - `b_ub`: Values on the right-hand side of the linear inequality 
          constraints.
        - `A_eq`: Matrix defining the coefficients of the linear equality 
          constraints, similar to `A_ub`.
        - `b_eq`: Values on the right-hand side of the linear equality 
          constraints, similar to `b_ub`.
        - `bounds`: Sequence of pairs (min, max) for each element in x, 
          determining the minimum and maximum values for that variable. By 
          default, it is a tuple (0, None) specifying non-negativity.
        - `method`: Optimization method, with the default being 'highs' 
          (previously 'simplex').
        - `callback`: Callback function executed once per iteration (not 
          needed in our case).
        - `options`: Dictionary of solver options (not needed in our case).
        - `x0`: Initial guess for the solution, to be refined during the 
          execution of the 'revised simplex' method.
        - `integrality`: Specifies the type of integrality constraint for each 
          solution variable: continuous (0), integer (1), semi-continuous (2), 
          semi-integer (3). By default, all variables are continuous.

    The output is an `OptimizeResult` object (`res`) containing:
        - `x`: 1-D array representing the values of variables minimizing the 
          objective function under the given constraints.
        - `fun`: Float representing the optimal value of the objective function.
        - `slack`: 1-D array representing the slack variables for linear 
          inequality constraints (b_ub - A_ub > 0).
        - `con`: 1-D array representing the slack variables for linear equality 
          constraints (b_eq - A_eq = 0).
        - `success`: Boolean indicating whether an optimal solution was found.
        - `status`: Integer indicating the status of the algorithm execution:
            - 0: Optimization successfully completed.
            - 1: Iteration limit reached.
            - 2: Problem appears to be infeasible.
            - 3: Problem appears to be unbounded.
            - 4: Numerical difficulties encountered.
        - `nit`: Integer representing the total number of iterations.
        - `message`: String providing a textual explanation of the algorithm's 
          termination state.
    '''
    
    # If the minimum value of an element in the matrix is <= 0, add at least
    # that much to make the optimization work
    matrix = copy.deepcopy(payoff_matrix)
    minelem = np.amin(matrix)
    correcting_val = 0
    if minelem <= 0:
        correcting_val = abs(minelem) + 1
        matrix += correcting_val
    
    # First player

    # If we want to maximize the value of our function, we should take values 
    # with the opposite sign from the right
    matrix_b_ub = (-1) * np.ones(np.shape(matrix)[1])

    # We take the matrix of coefficients with a "-" sign and transpose it because 
    # the coefficients for the 1st player are columns
    matrix_A_ub = (-1) * matrix.transpose()

    # Coefficients of our function are all 1, so we simply take a set of ones
    matrix_c = np.ones(np.shape(matrix)[0])

    # Using the function
    res = sp.optimize.linprog(c = matrix_c, A_ub = matrix_A_ub, b_ub = matrix_b_ub)
    
    # Checking the correctness of the function execution
    if res.status == 1:
        print("Iteration limit reached")
        return
    elif res.status == 2:
        print("Error")
        return
    elif res.status == 3:
        print("Out of bounds")
        return
    elif res.status == 4:
        print("Cannot compute")
        return
    else:
        value = res.fun
        p = res.x/value
        
    
    # Second player
    
    # If we want to minimize the value of our function, we should maximize 
    # the value of the inverse function =>
    # Coefficients of our function are all 1, so we simply take a set of ones * (-1)
    matrix_c = (-1) * np.ones(np.shape(matrix)[1])

    matrix_b_ub = np.ones(np.shape(matrix)[0])

    # We take the matrix of coefficients with a "+" sign, but we do not transpose it, 
    # because the coefficients for the 2nd player are rows
    matrix_A_ub = matrix

    # Using the function
    res = sp.optimize.linprog(c = matrix_c, A_ub = matrix_A_ub, 
                              b_ub = matrix_b_ub, method = 'highs')
    
    # Check the correctness of the function execution
    if res.status == 1:
        print("Iteration limit reached")
        return
    elif res.status == 2:
        print("Error")
        return
    elif res.status == 3:
        print("Out of bounds")
        return
    elif res.status == 4:
        print("Cannot compute")
        return
    else:
        q = res.x/value
    
    matrix -= correcting_val
    return (1/value - correcting_val, p, q)


def visualize(matrix: np.ndarray, spectrum: Tuple[np.ndarray, np.ndarray]):
    """
    Visualizes the spectrum of optimal strategies
    of the matrix game with the "spectrum" spectrum
    
    Parameters:
    - matrix (np.ndarray): payoff matrix for the game
    - spectrum (Tuple[np.ndarray, np.ndarray]): 
    spectrum of optimal strategies represented by a tuple,
    where the first element is the 1st player's strategies and 
    the second element is the 2nd player's strategies
    
    Returns:
    None
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Visualizing heatmap
    
    fig = plt.figure()
    plt.title('Heatmap for the game matrix')
    probability_matrix = spectrum[0][:, None] * spectrum[1]
    sns.heatmap(probability_matrix, annot=matrix, 
                fmt='d', linecolor='black', linewidth=0.01,
                annot_kws={'size': 13},
                cbar_kws={'label': 'probability'},
                xticklabels = [x for x in range(1, len(spectrum[1]) + 1)],
                yticklabels = [y for y in range(1, len(spectrum[0]) + 1)])
    
    # Now visualizing the strategy spectrums
    fig = plt.figure(figsize=(14,7))
    plt.subplot(1, 2, 1)
    plt.ylabel('probability')
    for k in [0,1]:
        ax = plt.subplot(1, 2, k + 1)
        plt.xlabel('strategy #')
        plt.title(f'Optimal strategies of the player #{k + 1}')
        for i in range(1,len(spectrum[k]) + 1):
            plt.plot([i, i], [0, spectrum[k][i - 1]],
                     c=plt.cm.plasma(spectrum[k][i - 1] / 1.01))
        plt.scatter([x for x in range(1, len(spectrum[k]) + 1)], 
                    spectrum[k], s=100, cmap='plasma', c=spectrum[k], vmax = 1)
        plt.xticks(range(1, len(spectrum[k]) + 1))
        plt.yticks(np.linspace(0, 1, 26))
        ax.set_xlim(1 - 0.1, len(spectrum[k]) + 0.1)
        ax.set_ylim(0 - 0.01, max(spectrum[k]) + 0.05)
        plt.grid(axis='y')
    plt.show()