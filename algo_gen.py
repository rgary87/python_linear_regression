import random
import operator

import track
from car import Car
from shapely.geometry import Point
import neural_network
from trigonometrie import get_point_in_zone_x


def get_random_posneg_value():
    v = random.random() * 0.1
    v = -v if random.random() < 50 else v
    return v


class AlgoGen:
    def __init__(self, population, population_size, selection_size, lucky_few_size, mutation_chance,
                 mutation_rate) -> None:
        super().__init__()
        self.population = population
        self.population_size = population_size
        self.selection_size = selection_size
        self.lucky_few_size = lucky_few_size
        self.mutation_chance = mutation_chance
        self.mutation_rate = mutation_rate
        self.to_breed = population_size - selection_size - lucky_few_size - 1
        self.polygons = track.get_polygon_zones()

    def get_ordered_population_by_fitness(self, to_print):
        val = {}
        for i in range(len(self.population)):
            val[self.population[i]] = self.calc_fitness(self.population[i])
        val = sorted(val.items(), key=operator.itemgetter(1), reverse=True)
        print([x[1] for x in val]) if to_print else ''
        return val

    def selection(self, population: [Car]):
        select = population[:self.selection_size]
        luckies = []
        for i in range(self.lucky_few_size):
            luckies.append(random.choice(population))
        select.extend(luckies)
        select.append(select[0])
        return select

    def breed_child(self, p1: Car, p2: Car):
        child = Car(p1.track)
        for i in range(len(p1.theta_1)):
            child.theta_1[i] = p1.theta_1[i] if random.random() * 100 < 50 else p2.theta_1[i]
        for i in range(len(p1.theta_2)):
            child.theta_2[i] = p1.theta_2[i] if random.random() * 100 < 50 else p2.theta_2[i]
        return child

    def cross_breed(self, population: [Car]):
        childs = []
        for i in range(self.to_breed):
            childs.append(self.breed_child(random.choice(population), random.choice(population)))
        population.extend(childs)
        return population

    def mutate(self, car: Car):
        mut = 0
        for t1 in car.theta_1:
            if random.random() * 100 < self.mutation_rate:
                mut += 1
                t1 += get_random_posneg_value()
        for t2 in car.theta_2:
            if random.random() * 100 < self.mutation_rate:
                mut += 1
                t2 += get_random_posneg_value()
        # print(f'MUTATED {mut} TIMES !')
        return car

    def mutate_population(self, population: [Car]):
        for i in range(len(population)):
            if random.random() * 100 < self.mutation_chance:
                population[i] = self.mutate(population[i])

    def move_population(self):
        for car in self.population:
            best_move = neural_network.neural_network(car.get_sensors_value(), car.theta_1, car.theta_2) + 1
            car.order(best_move)
        self.population = [x[0] for x in self.get_ordered_population_by_fitness(False)]

    def do_one_cycle(self):
        # print('Cycle')
        self.population = self.selection(self.population)
        self.population = self.cross_breed(self.population)
        self.mutate_population(self.population[1:])
        self.population = [x[0] for x in self.get_ordered_population_by_fitness(True)]

    def calc_fitness(self, car: Car):
        car_in_zone = get_point_in_zone_x(self.polygons, car.position)
        if car_in_zone is None:
            car.active = False
            return -1
        return car_in_zone #* 400 + (car.position[0] * 1.3) + car.position[1]

    def count_active_car(self):
        cnt = 0
        for c in self.population:
            if c.active:
                cnt += 1
        return cnt
