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
        # [
        #     [-1.275, -1.678, +1.751, -0.929],
        #     [+0.974, -0.116, -0.186, -0.143],
        #     [+0.540, -0.284, -0.845, -0.974],
        #     [+0.457, +0.906, +1.322, +0.435],
        #     [-0.488, +0.142, -1.490, +0.427],
        #     [+1.093, -2.026, -0.438, +0.565],
        # ]
        self.theta_1 = np.random.randn(first_hidden_layer_size, input_layer_size + 1)
        self.theta_2 = np.random.randn(second_hidden_layer_size, first_hidden_layer_size + 1)
        self.theta_3 = np.random.randn(num_label, second_hidden_layer_size + 1)
        self.sensor_range = 800
        self.sensor_distances = [0, 0, 0, 0, 0]
        self.sensor_intersect_points = [(0, 0),(0, 0),(0, 0),(0, 0),(0, 0)]
        self.track = track
        self.active = True
        self.move_step = 1
        self.default_max_move_allowed = 5000
        self.move_done = self.default_max_move_allowed
        self.max_zone_entered = -1

        self.inner_sensor_rotation = sp.pi / 12
        self.outer_sensor_rotation = sp.pi / 6

        self.fitness_value = 0.

    def reset_values(self):
        self.position = [self.start_point[0], self.start_point[1]]
        self.rotation = 0.
        self.active = True
        self.move_done = self.default_max_move_allowed
        self.max_zone_entered = -1

    def order(self, direction):
        if not self.active:
            return
        self.move_done += 1
        if self.move_done == self.default_max_move_allowed:
            print("Too many moves done !")
            self.active = False
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
            # results = [self.p.apply_async(segment_intersect, (s, s_track)) for s_track in self.track]
            # intersect = [res.get(timeout=1) for res in results]
            # print(f'Intersect done : {intersect}')
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
                    self.sensor_intersect_points[sensor_idx] = (i[0], i[1])
            sensor_idx += 1
        for s in self.sensor_distances:
            if s > 1000:
                print(f'WEIRD DISTANCE ! s: {s}')
            if s < 30:
                self.active = False
                print(f"Last sensors values: {self.sensor_distances[0]} | {self.sensor_distances[1]} | {self.sensor_distances[2]} | {self.sensor_distances[3]} | {self.sensor_distances[4]} ")
                break
        # print(f'Distances: {self.sensor_distances}')

        # #######################################
        # THIS IS HERE TO NORMALIZE THE DISTANCES
        # #######################################
        # self.sensor_distances = Car.normalize(self.sensor_distances + [self.sensor_range])[:-1]
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
