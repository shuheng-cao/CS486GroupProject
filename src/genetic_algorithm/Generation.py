#!/usr/bin/env python3

import random
import math

class Generation():

    def __init__(self, population, selection, threshold):
        """
        Initializes a Generation of individuals/chromosomes.
        """
        self.population = population
        self.threshold = threshold
        self.generations = 0
        self.selection = selection

    def run(self):
        """
        This method will run the genetic algorithm on the population for the
        given number of generations.
        """
        last = None
        
        while True:
            # Sort the population of chromosomes by their fitness
            population_by_fitness = sorted(
                self.population, key=lambda gene: gene.get_fitness())
            fittest_member = population_by_fitness[-1]
            if last is not None and fittest_member.get_fitness() - last.get_fitness() <= self.threshold:
                return last
            else:
                return fittest_member
            print('Generation: {}'.format(self.generations))
            print([member.get_fitness() for member in population_by_fitness])
            # calculate how many members should be removed
            length = len(population_by_fitness)
            cut = math.floor(length * self.selection) 
            # Memebers in the population after selection
            fittest = population_by_fitness[cut:]
            # Shuffle and cross breed the fittest members.
            random.shuffle(fittest)
            new_gen = []
            for i in range(0, length - cut, 2):
                if i+1 < length - cut:
                    new_gen.append(fittest[i].cross(fittest[i + 1]))
                else:
                    new_gen.append(fittest[i])
            self.population = new_gen
            for chromosome in self.population:
                chromosome.recalculate_fitness()
            self.generations += 1