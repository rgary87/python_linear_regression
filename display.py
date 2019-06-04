import pygame

class Display:

    def __init__(self) -> None:
        super().__init__()

    def draw_all(lines, cars: [Car]):
        screen.fill(bgcolor)
        for line in lines:
            pygame.draw.aaline(screen, fgcolor, line[0], line[1])
        pygame.display.flip()
        for car in cars:
            draw_car(car.position, car.rotation)


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


    def draw_line(line):
        pygame.draw.aaline(screen, fgcolor, line[0], line[1])
        pygame.display.flip()
