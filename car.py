import math

import scipy as sp
import numpy as np
from enum import Enum
from trigonometrie import segment_intersect
from multiprocessing import Pool
from functools import partial

input_layer_size = 5
hidden_layer_size = 10
num_label = 3


class CarOrder(Enum):
    TURN_LEFT = 1
    FORWARD = 2
    TURN_RIGHT = 3


class Car:

    def __init__(self, position, rotation, track) -> None:
        super().__init__()
        self.position = position
        self.rotation = rotation
        self.rotation_rate = sp.pi / 8
        self.theta_1 = np.random.randn(hidden_layer_size, input_layer_size + 1)
        self.theta_2 = np.random.randn(num_label, hidden_layer_size + 1)
        self.sensor_distances = [0, 0, 0, 0, 0]
        self.track = track

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

    def get_sensors_value(self):
        self.sensor_distances = [10_000, 10_000, 10_000, 10_000, 10_000]
        sensors = [
            self.get_sensor_left_1(),
            self.get_sensor_left_2(),
            self.get_sensor_middle(),
            self.get_sensor_right_1(),
            self.get_sensor_right_2()
        ]
        sensor_idx = 0
        for s in sensors:
            with Pool(len(self.track)) as p:
                intersect = p.map(partial(segment_intersect, line2=s), self.track)
            for i in intersect:
                if i is not None:
                    dist = math.hypot(i[0] - self.position[0], i[1] - self.position[1])
                    if self.sensor_distances[sensor_idx] > dist:
                        self.sensor_distances[sensor_idx] = dist
            sensor_idx += 1

    def get_sensor_left_1(self):
        return Car.rotate_2d(
            sp.array([[self.position[0], self.position[1]], [self.position[0], self.position[1] + 50]]),
            sp.array([self.position[0], self.position[1]]),
            self.rotation - sp.pi / 6)

    def get_sensor_left_2(self):
        return Car.rotate_2d(
            sp.array([[self.position[0], self.position[1]], [self.position[0], self.position[1] + 50]]),
            sp.array([self.position[0], self.position[1]]),
            self.rotation - sp.pi / 12)

    def get_sensor_middle(self):
        return Car.rotate_2d(
            sp.array([[self.position[0], self.position[1]], [self.position[0], self.position[1] + 50]]),
            sp.array([self.position[0], self.position[1]]),
            self.rotation)

    def get_sensor_right_1(self):
        return Car.rotate_2d(
            sp.array([[self.position[0], self.position[1]], [self.position[0], self.position[1] + 50]]),
            sp.array([self.position[0], self.position[1]]),
            self.rotation + sp.pi / 6)

    def get_sensor_right_2(self):
        return Car.rotate_2d(
            sp.array([[self.position[0], self.position[1]], [self.position[0], self.position[1] + 50]]),
            sp.array([self.position[0], self.position[1]]),
            self.rotation + sp.pi / 12)

    @staticmethod
    def rotate_2d(pts, cnt, ang):
        """
        pts = {}
        Rotates points(n*2) about center cnt(2) by angle ang(1) in radian
        """
        return sp.dot(pts - cnt, sp.array([[sp.cos(ang), sp.sin(ang)], [-sp.sin(ang), sp.cos(ang)]])) + cnt
