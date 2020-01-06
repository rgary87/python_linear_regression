import random
import operator
from multiprocessing.pool import Pool

import numpy as np
import track
from car import Car
from shapely.geometry import Point
import neural_network as nn
from trigonometrie import get_point_in_zone_x

import color

def get_random_posneg_value():
    v = random.random() * 0.1
    v = -v if random.random() < 50 else v
    return v


class AlgoGen:
    def __init__(self, population, population_size, selection_size, lucky_few_size, mutation_chance,
                 mutation_rate, to_regenerate, polygon_zones) -> None:
        super().__init__()
        self.population = population
        self.population_size = population_size
        self.selection_size = selection_size
        self.lucky_few_size = lucky_few_size
        self.mutation_chance = mutation_chance
        self.mutation_rate = mutation_rate
        self.to_breed = population_size - selection_size - lucky_few_size - 1 - to_regenerate
        self.to_regenerate = to_regenerate
        self.polygons = polygon_zones

    def get_ordered_population_by_fitness(self, to_print):
        val = {}
        for i in range(len(self.population)):
            val[self.population[i]] = self.calc_fitness(self.population[i])
        val = sorted(val.items(), key=operator.itemgetter(1), reverse=True)
        print([x[1] for x in val]) if to_print else ''
        return val

    @staticmethod
    def get_fitness_sum(population : [Car]):
        fitness_sum = 0
        for car in population:
            fitness_sum += car.fitness_value
        return fitness_sum

    @staticmethod
    def select_based_on_fitness(population : [Car], fitness_sum):
        rand = np.random.random() * fitness_sum
        running_sum = 0
        for i in range(len(population)):
            running_sum += population[i].fitness_value
            if running_sum > rand:
                return population[i].clone()

    def selection(self, population: [Car]):
        select = [population[0].clone()]
        # THIS WOULD NEED A BIT OF DISTANCE-BASED SELECTION
        fitness_sum = self.get_fitness_sum(population)
        while True:
            if len(select) == self.population_size: break
            first_parent = self.select_based_on_fitness(population, fitness_sum)
            second_parent = self.select_based_on_fitness(population, fitness_sum)
            child = self.breed_child(first_parent, second_parent)
            if len(select) == self.population_size: break
            select.append(first_parent)
            if len(select) == self.population_size: break
            select.append(second_parent)
            if len(select) == self.population_size: break
            select.append(child)
        return select

    def breed_child(self, p1: Car, p2: Car):
        child = Car(p1.start_point, p1.track, None)
        for ts in range(len(child.all_thetas)):
            for ti in range(len(child.all_thetas[ts])):
                for tj in range(len(child.all_thetas[ts][ti])):
                    child.all_thetas[ts][ti][tj] = p1.all_thetas[ts][ti][tj] if random.random() * 100 < 50 else p2.all_thetas[ts][ti][tj]
                    child.fitness_value = -1
        return child

    def cross_breed(self, population: [Car]):
        children = []
        print(f'to_breed: ({self.population_size - len(self.population)})' )
        for i in range(self.population_size - len(self.population)):
            children.append(self.breed_child(population[i % len(population)], population[abs(int(len(population) - i - 1)) % len(population)]))
        population.extend(children)
        return population

    def mutate(self, car: Car):
        mut = 0
        no_mut = 0
        car.fitness_value = -1.
        for ts in range(len(car.all_thetas)):
            for ti in range(len(car.all_thetas[ts])):
                for tj in range(len(car.all_thetas[ts][ti])):
                    if random.random() * 100 < self.mutation_rate:
                        mut += 1
                        car.all_thetas[ts][ti][tj] += nn.get_random_value_within_boundaries()
                        car.all_thetas[ts][ti][tj] = nn.limit_theta_value_to_boundaries(car.all_thetas[ts][ti][tj])
                    else:
                        no_mut += 1
        print(f'MUTATED {mut} TIMES OVER {mut + no_mut}!')
        return car

    def mutate_population(self, population: [Car]):
        for i in range(len(population)):
            if random.random() * 100 < self.mutation_chance:
                population[i] = self.mutate(population[i])

    @staticmethod
    def move_car(car):
        if car.active:
            # best_move = nn.neural_network(car.get_sensors_value(), car.theta_1, car.theta_2, car.theta_3) + 1
            # car.order(best_move)
            car.order_per_values(nn.neural_network_return_all_values(car.get_sensors_value(), car.theta_1, car.theta_2, car.theta_3))

    def move_population(self):
        [self.move_car(car) for car in self.population]
        self.population = [x[0] for x in self.get_ordered_population_by_fitness(False)]

    def do_one_cycle(self):
        # print('Cycle')
        print(f'{color.OKBLUE}Population fitness before selection new generation{color.ENDC}')
        self.population = [x[0] for x in self.get_ordered_population_by_fitness(True)]
        # ------------------------------------------------------------
        print(f'Population size for selection = {len(self.population)}')
        self.population = self.selection(self.population)
        # ------------------------------------------------------------
        # print(f'Population size for cross_breed = {len(self.population)}')
        # self.population = self.cross_breed(self.population)
        # ------------------------------------------------------------
        print(f'Population size for mutate_population = {len(self.population[1:])}')
        self.mutate_population(self.population[1:])
        # ------------------------------------------------------------
        print(f'{color.OKBLUE}Population fitness after new generation{color.ENDC}')
        self.population = [x[0] for x in self.get_ordered_population_by_fitness(True)]
        print(f'Population size after cycle = {len(self.population)}')

    def calc_fitness(self, car: Car):
        if not car.active:
            return car.fitness_value
        car_in_zone = get_point_in_zone_x(self.polygons, car.position)
        if car_in_zone is None or car_in_zone < car.max_zone_entered:
            print(f"U-turns are BAD. You were in zone {car.max_zone_entered} but returned to {car_in_zone}")
            car.active = False
            car.fitness_value = -1.
            car.max_zone_entered = car_in_zone
            return -1.
        car.max_zone_entered = car_in_zone
        # return car_in_zone #* 400 + (car.position[0] * 1.3) + car.position[1]
        car.fitness_value = max(0., (float(car_in_zone) * 100.) - (float(car.move_done) / 10.) + 450.)
        # car.fitness_value = float(car_in_zone * (float(car.move_done) / float(car.default_max_move_allowed)))
        return car.fitness_value

    def count_active_car(self):
        cnt = 0
        for c in self.population:
            if c.active:
                cnt += 1
        return cnt
