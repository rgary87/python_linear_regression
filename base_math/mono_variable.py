import numpy as np


def try_linear_algebra():
    x = np.array([18, 14, 9, 10, 5, 22, 14, 12])
    x_mean = np.mean(x)
    y = np.array([39, 9,9,7,8,35,36,22])
    y_mean = np.mean(y)

    diffs = 0.
    for i in range(len(x)):
        diffs += (x[i] - x_mean) * (y[i] - y_mean)
    squared_x_diff= 0.
    for i in x:
        squared_x_diff += pow(i - x_mean, 2)
    slope = diffs / squared_x_diff          # The line slope on a the graph
    intercept = y_mean - (slope * x_mean)   # The Y value when X is 0
    return slope, intercept


def linear_least_square(x, slope, intercept):
    return intercept + (slope * x)


if __name__ == '__main__':
    slope, intercept = try_linear_algebra()
    for i in range(30):
        print(f'Estimated value for %d: %.2f' % (i, linear_least_square(i, slope, intercept)))
