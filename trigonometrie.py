import numpy as np
import scipy as sp
import pygame


def rotate_2d(pts, cnt, ang=sp.pi / 8):
    '''pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian'''
    return sp.dot(pts - cnt, sp.array([[sp.cos(ang), sp.sin(ang)], [-sp.sin(ang), sp.cos(ang)]])) + cnt


class Car:

    def __init__(self, position, rotation) -> None:
        super().__init__()
        self.position = position
        self.rotation = rotation
        self.rotation_rate = sp.pi / 8

    def move_forward(self):

        points = rotate_2d(
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

def slope(p1, p2):
    return (p2[1] - p1[1]) * 1. / (p2[0] - p1[0])


def y_intercept(slope, p1):
    return p1[1] - 1. * slope * p1[0]


def intersect(line1, line2):
    min_allowed = 1e-5  # guard against overflow
    big_value = 1e10  # use instead (if overflow would have occurred)
    m1 = slope(line1[0], line1[1])
    print('m1: %d' % m1)
    b1 = y_intercept(m1, line1[0])
    print('b1: %d' % b1)
    m2 = slope(line2[0], line2[1])
    print('m2: %d' % m2)
    b2 = y_intercept(m2, line2[0])
    print('b2: %d' % b2)
    if abs(m1 - m2) < min_allowed:
        x = big_value
    else:
        x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    y2 = m2 * x + b2
    return (int(x), int(y))


def segment_intersect(line1, line2):
    intersection_pt = intersect(line1, line2)

    # print( line1[0][0], line1[1][0], line2[0][0], line2[1][0], intersection_pt[0] )
    # print( line1[0][1], line1[1][1], line2[0][1], line2[1][1], intersection_pt[1] )

    if (line1[0][0] < line1[1][0]):
        if intersection_pt[0] < line1[0][0] or intersection_pt[0] > line1[1][0]:
            return None
    else:
        if intersection_pt[0] > line1[0][0] or intersection_pt[0] < line1[1][0]:
            return None

    if (line2[0][0] < line2[1][0]):
        if intersection_pt[0] < line2[0][0] or intersection_pt[0] > line2[1][0]:
            return None
    else:
        if intersection_pt[0] > line2[0][0] or intersection_pt[0] < line2[1][0]:
            return None

    return intersection_pt


def draw_all(lines, cars: [Car]):
    screen.fill(bgcolor)
    for line in lines:
        pygame.draw.aaline(screen, fgcolor, line[0], line[1])
    pygame.display.flip()
    for car in cars:
        draw_car(car.position, car.rotation)

    # line1 = rotate_2d(sp.array([[line1[0][0], line1[0][1]], [line1[1][0], line1[1][1]]]),


#                           sp.array([line1[0][0], line1[0][1]]))
#         line1 = [(int(line1[0][0]), int(line1[0][1])), (line1[1][0], line1[1][1])]

def draw_car(position_vector, rotation):
    car_length = 50
    car_width = 25
    corner_top_left = [position_vector[0] + 0, position_vector[1] + 0]
    corner_top_right = [position_vector[0] + car_width, position_vector[1] + 0]
    corner_bottom_right = [position_vector[0] + car_width, position_vector[1] + car_length]
    corner_bottom_left = [position_vector[0] + 0, position_vector[1] + car_length]
    center = [position_vector[0] + int(car_width / 2), position_vector[1] + int(car_length / 2)]
    corners = sp.array([
        corner_top_left,
        corner_top_right,
        corner_bottom_left,
        corner_bottom_right,
    ])
    lines = rotate_2d(
        corners,
        center,
        rotation
    )
    corner_top_left = (int(lines[0][0]), int(lines[0][1]))
    corner_top_right = (int(lines[1][0]), int(lines[1][1]))
    corner_bottom_right = (int(lines[2][0]), int(lines[2][1]))
    corner_bottom_left = (int(lines[3][0]), int(lines[3][1]))

    pygame.draw.lines(screen, fgcolor, True,
                      [corner_top_left, corner_top_right, corner_bottom_left, corner_bottom_right])
    pygame.display.flip()

    # pygame.draw.aaline(screen, fgcolor, True, lines[0][0], int(line[1]))

    # for line in lines:
    #     pygame.draw.aaline(screen, fgcolor, True, int(line[0]), int(line[1]))


def draw_line(line):
    pygame.draw.aaline(screen, fgcolor, line[0], line[1])
    pygame.display.flip()


if __name__ == '__main__':
    # window dimensions
    w = 800
    h = 800
    # slightly off-white background
    bgcolor = (0xf1, 0xf2, 0xf3)
    # black for drawing
    fgcolor = (0, 0, 0)
    # red for "active" segment endpt
    redcolor = (0xff, 0, 0)
    # CPU throttle, higher number = less CPU hogging
    delay = 200
    # key repeat delay, interval
    key_delay = 20
    key_interval = 20

    # using +1 here to avoid using -1 elsewhere
    screen = pygame.display.set_mode((w + 1, h + 1))
    clock = pygame.time.Clock()
    pygame.key.set_repeat(key_delay, key_interval)

    line00 = [(100, 100), (118, 240)]
    line01 = [(118, 240), (239, 336)]
    line02 = [(239, 336), (405, 350)]
    line03 = [(405, 350), (534, 287)]
    line04 = [(534, 287), (568, 299)]
    line05 = [(568, 299), (584, 439)]
    line06 = [(584, 439), (485, 503)]
    line07 = [(485, 503), (268, 468)]
    line08 = [(268, 468), (63, 520)]
    line09 = [(63, 520), (90, 637)]
    line10 = [(90, 637), (237, 698)]
    line11 = [(237, 698), (488, 726)]
    line12 = [(488, 726), (675, 709)]
    line13 = [(675, 709), (766, 611)]

    line14 = [(247, 99), (249, 224)]
    line15 = [(249, 224), (401, 243)]
    line16 = [(401, 243), (515, 176)]
    line17 = [(515, 176), (675, 157)]
    line18 = [(675, 157), (736, 240)]
    line19 = [(736, 240), (758, 359)]
    line20 = [(758, 359), (746, 461)]
    line21 = [(746, 461), (618, 564)]
    line22 = [(618, 564), (444, 595)]
    line23 = [(444, 595), (394, 572)]
    line24 = [(394, 572), (213, 571)]
    line25 = [(213, 571), (221, 590)]
    line26 = [(221, 590), (312, 630)]
    line27 = [(312, 630), (487, 644)]
    line28 = [(487, 644), (645, 581)]
    line29 = [(645, 581), (700, 517)]
    # line30 = [(700, 517), (766, 611)]

    all_border_lines = [
        line00, line01, line02, line03, line04, line05, line06, line07, line08, line09,
        line10, line11, line12, line13, line14, line15, line16, line17, line18, line19,
        line20, line21, line22, line23, line24, line25, line26, line27, line28, line29,
    ]

    car = Car([179, 103], 0.)


    draw_all(all_border_lines, [car])

    active_pt = 0
    prev_active_pt = 0
    running = True

    pos = ''
    pos1 = None
    pos2 = None
    i = 30
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # print(f'event.type={event.type}')
                # print(f'event.key={event.key}')
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_UP:
                    car.move_forward()
                if event.key == pygame.K_LEFT:
                    car.turn_left()
                if event.key == pygame.K_RIGHT:
                    car.turn_right()

                draw_all(all_border_lines, [car])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos1 = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                pos = f'line{i} = [({pygame.mouse.get_pos()[0]}, {pygame.mouse.get_pos()[1]}), '
            elif event.type == pygame.MOUSEBUTTONUP:
                pos2 = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                all_border_lines.append([pos1, pos2])
                draw_all(all_border_lines, [car])
                print(f'{pos}({pygame.mouse.get_pos()[0]}, {pygame.mouse.get_pos()[1]})]')
                i += 1

        # sleep
        clock.tick(delay)
