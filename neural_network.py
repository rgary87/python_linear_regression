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


def neural_network(X, theta_1, theta_2):
    # input_layer_size = 5
    # hidden_layer_size = 10
    # num_label = 3
    #
    # theta_1 = np.random.randn(hidden_layer_size, input_layer_size + 1)
    # theta_2 = np.random.randn(num_label, hidden_layer_size + 1)

    h1 = sigmoid(np.dot(np.append([1], X), np.transpose(theta_1)))
    h2 = sigmoid(np.dot(np.append([1], h1), np.transpose(theta_2)))
    return get_higher_index(h2), [theta_1, theta_2]


