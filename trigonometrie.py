import numpy as np
import scipy as sp
import pygame
from car import *


# def slope(p1, p2):
#     if p2[0] == 179:
#         i = 0
#     print(f'p1[0]: {p1[0]}'
#           f' | p1[1]: {p1[1]}')
#     print(f'p2[0]: {p2[0]}'
#           f' | p2[1]: {p2[1]}')
#     return (p2[1] - p1[1]) * 1. / (p2[0] - p1[0])
#
#
# def y_intercept(slope, p1):
#     return p1[1] - 1. * slope * p1[0]
#
#
# def intersect(line1, line2):
#     min_allowed = 1e-5  # guard against overflow
#     big_value = 1e10  # use instead (if overflow would have occurred)
#     m1 = slope(line1[0], line1[1])
#     # print('m1: %d' % m1)
#     b1 = y_intercept(m1, line1[0])
#     # print('b1: %d' % b1)
#     m2 = slope(line2[0], line2[1])
#     # print('m2: %d' % m2)
#     b2 = y_intercept(m2, line2[0])
#     # print('b2: %d' % b2)
#     if abs(m1 - m2) < min_allowed:
#         x = big_value
#     else:
#         x = (b2 - b1) / (m1 - m2)
#     y = m1 * x + b1
#     y2 = m2 * x + b2
#     return (int(x), int(y))


# def segment_intersect(line1, line2):
#     print('segment_intersect !')
#     intersection_pt = intersect(line1, line2)
#
#     # print( line1[0][0], line1[1][0], line2[0][0], line2[1][0], intersection_pt[0] )
#     # print( line1[0][1], line1[1][1], line2[0][1], line2[1][1], intersection_pt[1] )
#
#     if line1[0][0] < line1[1][0]:
#         if intersection_pt[0] < line1[0][0] or intersection_pt[0] > line1[1][0]:
#             return None
#     else:
#         if intersection_pt[0] > line1[0][0] or intersection_pt[0] < line1[1][0]:
#             return None
#
#     if line2[0][0] < line2[1][0]:
#         if intersection_pt[0] < line2[0][0] or intersection_pt[0] > line2[1][0]:
#             return None
#     else:
#         if intersection_pt[0] > line2[0][0] or intersection_pt[0] < line2[1][0]:
#             return None
#
#     return intersection_pt


def segment_intersect(line1, line2):

    s1_x = line1[1][0] - line1[0][0]
    s1_y = line1[1][1] - line1[0][1]
    s2_x = line2[1][0] - line2[0][0]
    s2_y = line2[1][1] - line2[0][1]

    s = (-s1_y * (line1[0][0] - line2[0][0]) + s1_x * (line1[0][1] - line2[0][1])) / (-s2_x * s1_y + s1_x * s2_y)
    t = (s2_x * (line1[0][1] - line2[0][1]) - s2_y * (line1[0][0] - line2[0][0])) / (-s2_x * s1_y + s1_x * s2_y)

    if 0 <= s <= 1 and 0 <= t <= 1:
        # Collision detected
        i_x = line1[0][0] + (t * s1_x)
        i_y = line1[0][1] + (t * s1_y)
        # print('INTERSECTED !')
        return i_x, i_y

    return None # No collision

