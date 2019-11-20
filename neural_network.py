import numpy as np
from scipy.special import expit as sigmoid


def get_higher_index(tab: []):
    val = 0
    index = -1
    for i in range(len(tab)):
        if val < tab[i]:
            val = tab[i]
            index = i
    return index


def neural_network(X, theta_1, theta_2, theta_3):
    h1 = sigmoid(np.dot(np.append([1], X), np.transpose(theta_1)))
    h2 = sigmoid(np.dot(np.append([1], h1), np.transpose(theta_2)))
    h3 = sigmoid(np.dot(np.append([1], h2), np.transpose(theta_3)))
    return get_higher_index(h3)


def limit_theta_value_to_boundaries(val) -> float:
    if -1 < val < 1:
        return val
    if val < 0:
        return val + 1
    else:
        return val - 1


def get_random_value_within_boundaries() -> float:
    return 2 * np.random.random() - 1
