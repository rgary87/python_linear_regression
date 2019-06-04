import pygame
from car import *


class Display:

    def __init__(self, track) -> None:
        super().__init__()
        self.w = 800
        self.h = 800
        # slightly off-white background
        self.bgcolor = (0xf1, 0xf2, 0xf3)
        # black for drawing
        self.fgcolor = (0, 0, 0)
        # red for "active" segment endpt
        self.redcolor = (0xff, 0, 0)
        # CPU throttle, higher number = less CPU hogging
        self.delay = 200
        # key repeat delay, interval
        self.key_delay = 20
        self.key_interval = 20
        self.screen = pygame.display.set_mode((self.w + 1, self.h + 1))
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(self.key_delay, self.key_interval)
        self.track = track
        self.cars = [Car([179, 103], 0.)] * 20
        self.draw_all(track, self.cars)

    def main_loop(self):
        running = True

        pos = ''
        pos1 = ()
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
                        self.cars[0].move_forward()
                    if event.key == pygame.K_LEFT:
                        self.cars[0].turn_left()
                    if event.key == pygame.K_RIGHT:
                        self.cars[0].turn_right()
                    self.draw_all(self.track, self.cars)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos1 = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    pos = f'line{i} = [({pygame.mouse.get_pos()[0]}, {pygame.mouse.get_pos()[1]}), '
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos2 = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    self.track.append([pos1, pos2])
                    self.draw_all(self.track, self.cars)
                    print(f'{pos}({pygame.mouse.get_pos()[0]}, {pygame.mouse.get_pos()[1]})]')
                    i += 1

            # sleep
            self.clock.tick(self.delay)

    def draw_all(self, lines, cars: [Car]):
        self.screen.fill(self.bgcolor)
        for line in lines:
            pygame.draw.aaline(self.screen, self.fgcolor, line[0], line[1])
        pygame.display.flip()
        for car in cars:
            self.draw_car(car.position, car.rotation)

    def draw_car(self, position_vector, rotation):
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
        lines = Car.rotate_2d(
            corners,
            center,
            rotation
        )
        corner_top_left = (int(lines[0][0]), int(lines[0][1]))
        corner_top_right = (int(lines[1][0]), int(lines[1][1]))
        corner_bottom_right = (int(lines[2][0]), int(lines[2][1]))
        corner_bottom_left = (int(lines[3][0]), int(lines[3][1]))

        pygame.draw.lines(self.screen, self.fgcolor, True,
                          [corner_top_left, corner_top_right, corner_bottom_left, corner_bottom_right])
        pygame.display.flip()

    def draw_line(self, line):
        pygame.draw.aaline(self.screen, self.fgcolor, line[0], line[1])
        pygame.display.flip()
