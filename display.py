import pygame
import track
import track2
import trigonometrie
from algo_gen import AlgoGen
from car import *
import display_draw_only
import cProfile

class Display:

    def __init__(self, start_point, track, zone_limits, polygon_zones) -> None:
        super().__init__()
        # DISPLAY VALUES
        self.debug = False

        # DIPLAY INFO
        self.w = 800
        self.h = 1200
        self.bgcolor = (0xf1, 0xf2, 0xf3)
        self.fgcolor = (0, 0, 0)
        self.greencolor = (0, 0xff, 0)
        self.redcolor = (0xff, 0, 0)
        self.delay = 20
        self.key_delay = 20
        self.key_interval = 20
        self.screen = pygame.display.set_mode((self.w + 1, self.h + 1))
        self.clock = pygame.time.Clock()
        pygame.font.init()
        pygame.key.set_repeat(self.key_delay, self.key_interval)
        self.myfont = pygame.font.SysFont('Arial', 20)

        # TRACK INFO
        population_size = 50
        self.track = track
        self.zone_limits = zone_limits
        self.polygon_zones = polygon_zones
        self.start_point = start_point
        self.cars = [Car(self.start_point, self.track) for i in range(population_size)]
        self.gen = 1

        # ALGO GEN INFO
        self.algo_gen = AlgoGen(self.cars, population_size, int(population_size * 0.15), int(population_size * 0.15),
                                30, 50, 0, self.polygon_zones)

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
        tmp = self.algo_gen.count_active_car()
        # self.algo_gen.do_one_cycle()
        # self.algo_gen.move_population()
        intersect_lines = self.track.copy()
        print(f'Car count: {self.algo_gen.count_active_car()}')

        compute = True

        while running:
            # print('while running')
            if self.gen > 40:
                break
            if compute:
                if self.is_any_active_car():
                    if self.algo_gen.count_active_car() != tmp:
                        print(f'Car count: {self.algo_gen.count_active_car()}')
                        tmp = self.algo_gen.count_active_car()
                    self.algo_gen.move_population()
                else:
                    self.gen += 1
                    print('no moving car anymore...')
                    self.algo_gen.do_one_cycle()
                    for p in self.algo_gen.population:
                        p.reset_values()
                    tmp = self.algo_gen.count_active_car()
            for event in pygame.event.get():
                # print('if for event')
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    print(f'event.type={event.type}')
                    print(f'event.key={event.key}')
                    if event.key == pygame.K_q:
                        running = False
                    if event.key == pygame.K_r and compute:
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
                    if event.key == pygame.K_EQUALS:
                        print(f'self.algo_gen.mutation_rate: {self.algo_gen.mutation_rate}')
                        self.algo_gen.mutation_rate += 10
                        print(f'self.algo_gen.mutation_rate: {self.algo_gen.mutation_rate}')
                    if event.key == pygame.K_MINUS:
                        print(f'self.algo_gen.mutation_rate: {self.algo_gen.mutation_rate}')
                        self.algo_gen.mutation_rate -= 10
                        print(f'self.algo_gen.mutation_rate: {self.algo_gen.mutation_rate}')
                    if event.key == pygame.K_d:
                        self.debug = not self.debug
                    if event.key == pygame.K_s:
                        compute = not compute

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
        self.draw_theta_table()
        for line in lines:
            pygame.draw.aaline(self.screen, self.fgcolor, line[0], line[1])
        for car in cars:
            self.draw_car(car.position, car.rotation, car.active)
        self.draw_text_info()
        self.draw_zones_limits()
        self.draw_zones_number()
        pygame.display.flip()

    def draw_car(self, position_vector, rotation, active):
        car_length = 50
        car_width = 25
        corner_top_left = [position_vector[0] - int(car_width / 2), position_vector[1] - int(car_length / 2)]
        corner_top_right = [position_vector[0] + int(car_width / 2), position_vector[1] - int(car_length / 2)]
        corner_bottom_right = [position_vector[0] + int(car_width / 2), position_vector[1] + int(car_length / 2)]
        corner_bottom_left = [position_vector[0] - int(car_width / 2), position_vector[1] + int(car_length / 2)]
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
            pygame.draw.lines(self.screen, self.greencolor, True, [corner_top_left, corner_top_right, corner_bottom_left, corner_bottom_right])
        else:
            pygame.draw.lines(self.screen, self.redcolor, True, [corner_top_left, corner_top_right, corner_bottom_left, corner_bottom_right])

    def draw_zones_limits(self):
        if not self.debug:
            return
        for l in self.zone_limits:
            self.draw_line(l)

    def draw_line(self, line):
        pygame.draw.aaline(self.screen, self.fgcolor, line[0], line[1])

    def draw_text_info(self):
        textsurface = self.myfont.render( f'Generation {self.gen} | Mutation Change {self.algo_gen.mutation_chance} | Mutation Rate {self.algo_gen.mutation_rate}', True, self.fgcolor)
        self.screen.blit(textsurface, (150, 25))

    def draw_zones_number(self):
        if not self.debug:
            return
        i = 0
        for p in self.polygon_zones:
            textsurface = self.myfont.render(f'{i}', True, self.fgcolor)
            point = p.centroid
            self.screen.blit(textsurface, (point.coords[0][0], point.coords[0][1]))
            i += 1

    def draw_theta_table(self):
        self.draw_line([(0, 800), (800, 800)])
        cell_width = int(760 / (input_layer_size + 1))
        cell_height = int(360 / (first_hidden_layer_size))
        for i in range(input_layer_size + 1):
            for j in range(first_hidden_layer_size):
                pos_x_start = 20 + (i * cell_width)
                pos_y_start = 820 + (j * cell_height)
                pygame.draw.rect(self.screen, self.fgcolor, pygame.Rect((pos_x_start, pos_y_start, cell_width, cell_height)), 1)
                if self.algo_gen.population[0].theta_1[j][i] > 0:
                    textsurface = self.myfont.render(f'{self.algo_gen.population[0].theta_1[j][i]:1.3f}', True, self.greencolor)
                else:
                    textsurface = self.myfont.render(f'{self.algo_gen.population[0].theta_1[j][i]:1.3f}', True, self.redcolor)
                self.screen.blit(textsurface, (pos_x_start + int(cell_width / 2) - 5, pos_y_start + int(cell_height / 2)))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "draw":
        display = display_draw_only.DisplayOnlyDraw(track2.get_track())
        display.main_loop()
    else:
        display = Display(track2.get_start_point(), track2.get_track(), track2.get_zones_limits(), track2.get_polygon_zones())
        display.main_loop()

