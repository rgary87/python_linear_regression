import numpy as np


def normalize_value(x):
    x_2 = x / np.std(x)
    # x_2 = x.copy()
    # max_x = np.max(x)
    # min_x = np.min(x)
    # for i in range(len(x)):
    #     x_2[i] = (x[i] - min_x) / (max_x - min_x)
    return x_2


def try_multivariable_linear_regression(Xs: [[]], y: []):
    arr = np.ones((len(Xs[0]), 1))
    for i in range(len(Xs)):
        arr = np.insert(arr, [i + 1], Xs[i], axis=1)
    arr_mean = np.mean(arr, axis=0)


    tmp1 = np.dot(np.transpose(arr), arr)
    tmp2 = np.dot(tmp1, np.transpose(arr))
    tmp3 = np.dot(tmp2, y)
    i = 0
    # x_matrix = np.matrix()



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
    var_y = [16.68,
             11.50,
             12.03,
             14.88,
             13.75,
             18.11]
    var_x_1 = normalize_value(var_x_1)
    var_x_2 = normalize_value(var_x_2)
    try_multivariable_linear_regression([var_x_1, var_x_2], var_y)

