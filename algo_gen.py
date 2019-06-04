import random
import operator

import track
from car import Car
from shapely.geometry import Point
import neural_network


def get_random_posneg_value():
    v = random.random()
    v = v * -1 if random.random() < 50 else v
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
        self.to_breed = population_size - selection_size - lucky_few_size
        self.polygons = track.get_polygon_zones()

    def selection(self, population: [Car]):
        val = {}
        for i in range(len(population)):
            val[population[i]] = self.calc_fitness(population[i])
        val = sorted(val.items(), key=operator.itemgetter(1))
        select = val[:self.selection_size]
        luckies = []
        for i in range(self.lucky_few_size):
            luckies.append(random.choice(val))
        select.extend(luckies)
        return select

    def breed_child(self, p1: Car, p2: Car):
        child = Car(p1.position, p1.rotation, p1.track)
        for i in range(len(p1.theta_1)):
            child.theta_1[i] = p1.theta_1[i] if random.random() * 100 < 50 else p2.theta_1[i]
        for i in range(len(p1.theta_2)):
            child.theta_2[i] = p1.theta_2[i] if random.random() * 100 < 50 else p2.theta_2[i]

    def cross_breed(self, population: [Car]):
        for i in range(self.to_breed):
            population.append(self.breed_child(random.choice(population), random.choice(population)))
        return population

    def mutate(self, car: Car):
        for t1 in car.theta_1:
            if random.random() * 100 < self.mutation_rate:
                t1 += get_random_posneg_value()
        for t2 in car.theta_2:
            if random.random() * 100 < self.mutation_rate:
                t2 += get_random_posneg_value()
        return car

    def mutate_population(self, population: [Car]):
        for i in range(len(population)):
            if random.random() < self.mutation_chance:
                population[i] = self.mutate(population[i])
        return population

    def move_population(self, population):
        for car in population:
            best_move = neural_network.neural_network(car.get_sensors_value(), car.theta_1, car.theta_2) + 1
            car.order(best_move)

    def do_one_cycle(self):
        self.population = self.selection(self.population)
        self.population = self.cross_breed(self.population)
        self.population = self.mutate_population(self.population)
        self.move_population(self.population)

    def calc_fitness(self, car: Car):
        return self.get_point_in_zone_x(car.position) * 200 + car.position[0] + car.position[1]

    def get_point_in_zone_x(self, position):
        p = Point(position[0], position[1])
        for i in range(len(self.polygons)):
            if self.polygons[i].contains(p):
                return i
