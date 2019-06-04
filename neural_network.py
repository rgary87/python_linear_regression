import numpy as np
import costFunction as cf


def get_higher_index(tab: []):
    val = 0
    index = -1
    for i in range(len(tab)):
        if val < tab[i]:
            val = tab[i]
            index = i
    return index


def neural_network():
    X = np.array([
        15,
        25,
        100,
        25,
        15
    ])
    input_layer_size = 5
    first_hidden_layer_size = 10
    second_hidden_layer_size = 50
    num_label = 3

    theta_1 = np.random.randn(first_hidden_layer_size, input_layer_size + 1)
    theta_2 = np.random.randn(second_hidden_layer_size, first_hidden_layer_size + 1)
    theta_3 = np.random.randn(num_label, second_hidden_layer_size + 1)

    h1 = cf.sigmoid(np.dot(np.append([1], X), np.transpose(theta_1)))
    h2 = cf.sigmoid(np.dot(np.append([1], h1), np.transpose(theta_2)))
    h3 = cf.sigmoid(np.dot(np.append([1], h2), np.transpose(theta_3)))
    return get_higher_index(h3)


