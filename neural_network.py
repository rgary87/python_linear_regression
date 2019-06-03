import numpy as np

if __name__ == '__main__':
    input_layer_size = 400
    hidden_layer_size = 25
    num_label = 10

    theta_1 = np.random.randn(hidden_layer_size, input_layer_size + 1)
    theta_2 = np.random.randn(num_label, hidden_layer_size + 1)

    


