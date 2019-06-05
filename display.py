import pygame
import track
from algo_gen import AlgoGen
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
        # green for "active" car
        self.greencolor = (0, 0xff, 0)
        # red for "deactive" car
        self.redcolor = (0xff, 0, 0)
        # CPU throttle, higher number = less CPU hogging
        self.delay = 200
        # key repeat delay, interval
        self.key_delay = 20
        self.key_interval = 20
        self.screen = pygame.display.set_mode((self.w + 1, self.h + 1))
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        pygame.key.set_repeat(self.key_delay, self.key_interval)
        self.gen = 1
        self.track = track
        self.cars = [Car(track) for i in range(30)]
        self.draw_all(track, self.cars)
        self.algo_gen = AlgoGen(self.cars, 30, 8, 2, 20, 10)

    def is_any_active_car(self):
        for c in self.algo_gen.population:
            if c.active:
                return True
        return False

    def main_loop(self):
        running = True

        pos = ''
        pos1 = ()
        i = 30
        # self.algo_gen.do_one_cycle()
        # self.algo_gen.move_population()
        intersect_lines = self.track.copy()

        while running:
            # print('while running')

            if self.is_any_active_car():
                print(f'Car count: {self.algo_gen.count_active_car()}')
                self.algo_gen.move_population()
            else:
                self.gen += 1
                print('no moving car anymore...')
                self.algo_gen.do_one_cycle()
                for p in self.algo_gen.population:
                    p.reset_values()
            for event in pygame.event.get():
                # print('if for event')
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    # print(f'event.type={event.type}')
                    # print(f'event.key={event.key}')
                    if event.key == pygame.K_q:
                        running = False
                    if event.key == pygame.K_r:
                        self.algo_gen.do_one_cycle()
                        for p in self.algo_gen.population:
                            p.reset_values()
                    if event.key == pygame.K_UP:
                        self.cars[0].move_forward()
                        self.cars[0].get_sensors_value()
                        intersect_lines = self.track.copy()
                        intersect_lines.extend(self.cars[0].sensors)
                    if event.key == pygame.K_LEFT:
                        self.cars[0].turn_left()
                    if event.key == pygame.K_RIGHT:
                        self.cars[0].turn_right()
                    # self.draw_all(self.track, self.cars)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos1 = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    pos = f'line{i} = [({pygame.mouse.get_pos()[0]}, {pygame.mouse.get_pos()[1]}), '
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos2 = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    self.track.append([pos1, pos2])
                    # self.draw_all(self.track, self.cars)
                    print(f'{pos}({pygame.mouse.get_pos()[0]}, {pygame.mouse.get_pos()[1]})]')
                    i += 1

            self.draw_all(intersect_lines, self.algo_gen.population)
            # sleep
            self.clock.tick(self.delay)

    def draw_all(self, lines, cars: [Car]):
        self.screen.fill(self.bgcolor)
        for line in lines:
            pygame.draw.aaline(self.screen, self.fgcolor, line[0], line[1])
        for car in cars:
            self.draw_car(car.position, car.rotation, car.active)
        textsurface = self.myfont.render(f'Generation {self.gen}', False, self.fgcolor)
        self.screen.blit(textsurface, (50,50))
        pygame.display.flip()

    def draw_car(self, position_vector, rotation, active):
        car_length = 50
        car_width = 25
        corner_top_left = [position_vector[0] - int(car_width/2), position_vector[1] - int(car_length/2)]
        corner_top_right = [position_vector[0] + int(car_width/2), position_vector[1] - int(car_length/2)]
        corner_bottom_right = [position_vector[0] + int(car_width/2), position_vector[1] + int(car_length/2)]
        corner_bottom_left = [position_vector[0] - int(car_width/2), position_vector[1] + int(car_length/2)]
        center = [position_vector[0], position_vector[1]]
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

        if active:
            pygame.draw.lines(self.screen, self.greencolor, True,
                          [corner_top_left, corner_top_right, corner_bottom_left, corner_bottom_right])
        else:
            pygame.draw.lines(self.screen, self.redcolor, True,
                              [corner_top_left, corner_top_right, corner_bottom_left, corner_bottom_right])

    def draw_line(self, line):
        pygame.draw.aaline(self.screen, self.fgcolor, line[0], line[1])


if __name__ == '__main__':
    display = Display(track.get_track())
    display.main_loop()
