import math

import scipy as sp
import numpy as np
from enum import Enum
from trigonometrie import segment_intersect
from multiprocessing import Pool
from functools import partial

input_layer_size = 5
first_hidden_layer_size = 4
second_hidden_layer_size = 3
num_label = 2


class CarOrder(Enum):
    TURN_LEFT_SLOW_FORWARD = 4
    TURN_LEFT = 1
    FORWARD = 3
    TURN_RIGHT_SLOW_FORWARD = 5
    TURN_RIGHT = 2


class Car:

    def __init__(self, start_point, track) -> None:
        super().__init__()
        self.car_length = 50
        self.car_width = 25
        self.start_point = start_point
        self.position = start_point
        self.rotation = 0.
        self.rotation_rate = sp.pi / 48
        self.theta_1 = np.random.randn(first_hidden_layer_size, input_layer_size + 1)
        self.theta_2 = np.random.randn(second_hidden_layer_size, first_hidden_layer_size + 1)
        self.theta_3 = np.random.randn(num_label, second_hidden_layer_size + 1)
        self.sensor_range = 800
        self.sensor_distances = [0, 0, 0, 0, 0]
        self.track = track
        self.active = True
        self.move_step = 1

        self.inner_sensor_rotation = sp.pi / 12
        self.outer_sensor_rotation = sp.pi / 6

        # self.inner_sensor_rotation = sp.pi / 8
        # self.outer_sensor_rotation = sp.pi / 4

    def reset_values(self):
        self.position = [self.start_point[0], self.start_point[1]]
        self.rotation = 0.
        self.active = True

    def order(self, direction):
        if not self.active:
            return
        # print('MOVE !',end='')
        if direction == CarOrder.TURN_LEFT.value:
            self.turn_left()
            self.move_forward()
        elif direction == CarOrder.FORWARD.value:
            self.move_forward()
        elif direction == CarOrder.TURN_RIGHT.value:
            self.turn_right()
            self.move_forward()
        elif direction == CarOrder.TURN_LEFT_SLOW_FORWARD.value:
            self.turn_left()
            self.move_slow_forward()
        elif direction == CarOrder.TURN_RIGHT_SLOW_FORWARD.value:
            self.turn_right()
            self.move_slow_forward()

    def move_forward(self):
        points = Car.rotate_2d(
            sp.array([
                [self.position[0], self.position[1]],
                [self.position[0], self.position[1] + self.move_step]
            ]),
            sp.array([self.position[0], self.position[1]]),
            self.rotation
        )
        self.position = [points[1][0], points[1][1]]

    def move_slow_forward(self):
        points = Car.rotate_2d(
            sp.array([
                [self.position[0], self.position[1]],
                [self.position[0], self.position[1] + self.move_step]
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
        self.sensors = [
            self.get_sensor_left_1(),
            self.get_sensor_left_2(),
            self.get_sensor_middle(),
            self.get_sensor_right_1(),
            self.get_sensor_right_2()
        ]
        sensor_idx = 0
        for s in self.sensors:
            # with Pool(len(self.track)) as p:
            #     intersect = p.map(partial(segment_intersect, line2=s), self.track)
            intersect = []
            for s_track in self.track:
                inter = segment_intersect(s, s_track)
                if inter is not None:
                    intersect.append(inter)
            for i in intersect:
                dist = math.hypot(i[0] - self.position[0], i[1] - self.position[1])
                if self.sensor_distances[sensor_idx] > dist:
                    self.sensor_distances[sensor_idx] = dist
            sensor_idx += 1
        for s in self.sensor_distances:
            if s > 1000:
                print('WEIRD DISTANCE !')
            if s < 30:
                self.active = False
                break
        # print(f'Distances: {self.sensor_distances}')
        self.sensor_distances = Car.normalize(self.sensor_distances + [self.sensor_range])[:-1]
        return self.sensor_distances

    def get_sensor_left_1(self):
        return Car.rotate_2d(
            sp.array([[self.position[0], self.position[1]], [self.position[0], self.position[1] + self.sensor_range]]),
            sp.array([self.position[0], self.position[1]]),
            self.rotation - self.outer_sensor_rotation)

    def get_sensor_left_2(self):
        return Car.rotate_2d(
            sp.array([[self.position[0], self.position[1]], [self.position[0], self.position[1] + self.sensor_range]]),
            sp.array([self.position[0], self.position[1]]),
            self.rotation - self.inner_sensor_rotation)

    def get_sensor_middle(self):
        return Car.rotate_2d(
            sp.array([[self.position[0], self.position[1]], [self.position[0], self.position[1] + self.sensor_range]]),
            sp.array([self.position[0], self.position[1]]),
            self.rotation)

    def get_sensor_right_1(self):
        return Car.rotate_2d(
            sp.array([[self.position[0], self.position[1]], [self.position[0], self.position[1] + self.sensor_range]]),
            sp.array([self.position[0], self.position[1]]),
            self.rotation + self.outer_sensor_rotation)

    def get_sensor_right_2(self):
        return Car.rotate_2d(
            sp.array([[self.position[0], self.position[1]], [self.position[0], self.position[1] + self.sensor_range]]),
            sp.array([self.position[0], self.position[1]]),
            self.rotation + self.inner_sensor_rotation)

    @staticmethod
    def rotate_2d(pts, cnt, ang):
        """
        pts = {}
        Rotates points(n*2) about center cnt(2) by angle ang(1) in radian
        """
        return sp.dot(pts - cnt, sp.array([[sp.cos(ang), sp.sin(ang)], [-sp.sin(ang), sp.cos(ang)]])) + cnt

    @staticmethod
    def normalize(v):
        norm = np.linalg.norm(v, ord=1)
        if norm == 0:
            norm = np.finfo(v.dtype).eps
        return v / norm
