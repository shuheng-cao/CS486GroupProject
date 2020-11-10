#!/usr/bin/env python3

import random
import math

class Generation():

    def __init__(self, population, selection):
        """
        Initializes a Generation of individuals/chromosomes.
        """
        assert len(population) % 4 == 0
        self.population = population
        self.threshold = 1
        self.generations = 0
        self.selection = selection

    def run(self):
        """
        This method will run the genetic algorithm on the population for the
        given number of generations.
        """
        last = 0
        cut = math.floor(len(self.population) * self.selection)
        while True:
            # Sort the population of chromosomes by their fitness
            population_by_fitness = sorted(
                self.population, key=lambda gene: gene.get_fitness())
            fittest_member = population_by_fitness[-1]
            if fittest_member - last <= self.threshold:
                return fittest_member
            else:
                last = fittest_member
            print('Generation: {}'.format(self.generations))
            print([member.get_fitness() for member in population_by_fitness])
            # Select the top half of the fittest members.
            fittest = population_by_fitness[cut:]
            # Shuffle and cross breed the fittest members.
            random.shuffle(fittest)
            new_gen = []
            for i in range(0, len(population_by_fitness) - cut, 2):
                new_gen += [fittest[i].cross(fittest[i + 1])]
            self.population = new_gen
            for chromosome in self.population:
                chromosome.recalculate_fitness()
            self.generations += 1