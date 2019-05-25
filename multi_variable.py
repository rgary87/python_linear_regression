import time

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def normalize_value(x):
    row_sum = np.linalg.norm(x)
    norm_matrix = x / row_sum
    return norm_matrix

def compute_cost_function(X,y,theta):
    to_be_summed = np.power(((X @ theta.T)-y),2)
    return np.sum(to_be_summed)/(2 * len(X))


def try_multivariable_linear_regression(Xs: [[]], y: []):
    arr = np.ones((len(Xs[0]), 1))
    for i in range(len(Xs)):
        arr = np.insert(arr, [i + 1], Xs[i], axis=1)
    alpha = 0.1
    iters = 1000
    theta = np.zeros([1,len(arr[0])])
    print(f'First cost is: {compute_cost_function(arr, y, theta)}')
    theta, cost = gradient_descend(arr, y, theta, iters, alpha)
    print(f'Final cost is: {compute_cost_function(arr, y, theta)}')
    fig, ax = plt.subplots()
    ax.plot(np.arange(iters), cost, 'r')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Cost')
    ax.set_title('Error vs. Training Epoch')
    plt.show()

def gradient_descend(X: [[]], y: [], theta: [], iters: int, alpha: float):
    cost = np.zeros(iters)
    for i in range(iters):
        t1 = X * (X @ theta.T) - y
        t2 = np.sum(t1, axis=0)
        t3 = alpha/len(X)
        t4 = t3 * t2
        theta = theta - t4
        # theta = theta - (alpha/len(X)) * np.sum(X * (X @ theta.T - y), axis=0)
        cost[i] = compute_cost_function(X, y, theta)
        if i > 0 and cost[i] > cost[i-1]:
            alpha /= 2
    print(f'Alpha ends up: {alpha}')
    return theta, cost


if __name__ == '__main__':
    var_x_1 = [[7],
               [3],
               [3],
               [4],
               [6],
               [7]]
    var_x_2 = [[560],
               [220],
               [340],
               [80],
               [150],
               [330]]
    var_y = [[16.68],
             [11.50],
             [12.03],
             [14.88],
             [13.75],
             [18.11]]
    try_multivariable_linear_regression([normalize_value(var_x_1), normalize_value(var_x_2)], np.array(var_y))
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(var_x_1, var_y, zs=var_x_2)
    # # plt.plot(var_x_1, '.')
    # # plt.plot(var_x_2, '.')
    # plt.show()[
    # beta = try_multivariable_linear_algebra([var_x_1, var_x_2], var_y)
    # for i in range(len(var_x_1)):
    #     print(f'X1={var_x_1[i][0]}'
    #           f'|X2={var_x_2[i][0]}'
    #           f'|Y={beta[0] + (beta[1] * var_x_1[i][0]) + (beta[2] * var_x_2[i][0])}')