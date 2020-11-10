import Board
import Population
import Chromosome
import argparse
import pickle

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=argparse.FileType('rb'))
    parser.add_argument('--threshold', type=int, default=1)
    parser.add_argument('--population_size', type=int, default=16)
    parser.add_argument('--n_simulations', type=int,
                        default=Chromosome.N_SIMULATIONS)
    parser.add_argument('--mutation_chance', type=float,
                        default=Chromosome.MUTATION_CHANCE)
    args = parser.parse_args()

    genes = Chromosome.random_genes()
    if args.seed:
        with args.seed as seed:
            chromosome = pickle.load(seed)
            genes = chromosome.genes

    Chromosome.set_globals(args.n_simulations,
                           args.mutation_chance)
    population = Population([
        Chromosome(genes) for i in range(args.population_size)])
    fittest = population.run()
    print('Fittest member: {}'.format(fittest))

if __name__ == '__main__':
    main()