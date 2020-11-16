from Board import Field
from Generation import Generation
from Chromosome import Chromosome
import argparse

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--threshold', type=int, default=0)
    parser.add_argument('--population_size', type=int, default=50)
    parser.add_argument('--n_simulations', type=int, default=10)
    parser.add_argument('--mutation_chance', type=float, default=0.01)
    parser.add_argument('--selection_rate', type=float, default=0.4)
    args = parser.parse_args()

    Chromosome.set_globals(args.n_simulations,args.mutation_chance) # initialize macro for N and q
    population = Generation([Chromosome.random() for i in range(args.population_size)], args.selection_rate, args.threshold) # initialize macro for p and stopping_criteria
    fittest = population.run()
    print('Fittest member: {}'.format(fittest))

if __name__ == '__main__':
    main()