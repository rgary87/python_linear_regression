import scipy as sp
import numpy as np
from enum import Enum

input_layer_size = 5
hidden_layer_size = 10
num_label = 3


class CarOrder(Enum):
    TURN_LEFT = 1
    FORWARD = 2
    TURN_RIGHT = 3


class Car:

    def __init__(self, position, rotation) -> None:
        super().__init__()
        self.position = position
        self.rotation = rotation
        self.rotation_rate = sp.pi / 8
        self.theta_1 = np.random.randn(hidden_layer_size, input_layer_size + 1)
        self.theta_2 = np.random.randn(num_label, hidden_layer_size + 1)
        self.sensor_distances = [0, 0, 0, 0, 0]

    def order(self, direction):
        if direction == 1:
            self.turn_left()
        elif direction == 2:
            self.move_forward()
        else:
            self.turn_right()

    def move_forward(self):
        points = Car.rotate_2d(
            sp.array([
                [self.position[0], self.position[1]],
                [self.position[0], self.position[1] + 10]
            ]),
            sp.array([self.position[0], self.position[1]]),
            self.rotation
        )
        self.position = [points[1][0], points[1][1]]

    def turn_right(self):
        self.rotation += self.rotation_rate

    def turn_left(self):
        self.rotation -= self.rotation_rate

    @staticmethod
    def rotate_2d(pts, cnt, ang):
        """
        pts = {}
        Rotates points(n*2) about center cnt(2) by angle ang(1) in radian
        """
        return sp.dot(pts - cnt, sp.array([[sp.cos(ang), sp.sin(ang)], [-sp.sin(ang), sp.cos(ang)]])) + cnt

