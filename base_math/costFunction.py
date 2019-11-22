import numpy as np
from scipy.special import expit as sigmoid


def sigmoidGradient(z):
    g = np.zeros(len(z))
    g = sigmoid(z)
    g = np.dot(g, (1 - g))
    return g


def square_sum(n):
    return np.sum(np.sum([pow(x,2) for x in n[2:]]))


def regul_grad(lambda_var, m, n):
    return lambda_var / m * (np.zeros([len(n[0]), [x for x in n[2:]]]))


def nnCostFunction(theta_1, theta_2, num_label, X, y, lambda_var):
    m = len(X[0])
    J = 0
    theta_1_grad = np.zeros(len(theta_1))
    theta_2_grad = np.zeros(len(theta_2))

    Y = y[1:num_label]
    D = 0

    for i in range(1, m):
        z2 = [1, X[i]] * np.transpose(theta_1)
        hidden_layer = sigmoid(z2)
        output_layer = sigmoid([1, hidden_layer] * np.transpose(theta_2))

        Yi = Y[i]
        J += np.sum(np.dot(np.dot(-Yi, np.log(output_layer)) - (1 - Yi), np.log(1 - output_layer)))

        d3 = np.transpose(output_layer - Yi)
        d2 = np.dot(np.transpose(theta_2) * d3, sigmoidGradient([1, z2[:]]))
        theta_1_grad += d2[2:] * [1, X[i][:]]
        theta_2_grad += d3 * [1, hidden_layer[:]]

    regul = lambda_var / (2 * m) * (square_sum(theta_1) + square_sum(theta_2))
    J = 1 / m * J + regul
    theta_1_grad = 1 / m * theta_1_grad + regul_grad(lambda_var, m, theta_1)
    theta_2_grad = 1 / m * theta_2_grad + regul_grad(lambda_var, m, theta_2)
    return theta_1_grad, theta_2_grad
