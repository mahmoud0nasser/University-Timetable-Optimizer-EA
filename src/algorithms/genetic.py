"""
Genetic Algorithm implementation for university timetabling.
"""
import numpy as np
from typing import List, Tuple, Callable, Any
from dataclasses import dataclass
import random

@dataclass
class GeneticAlgorithmConfig:
    population_size: int = 50
    n_generations: int = 100
    mutation_rate: float = 0.1
    tournament_size: int = 3
    elite_size: int = 1

class Individual:
    def __init__(self, chromosome: np.ndarray):
        self.chromosome = chromosome
        self.fitness = float('inf')

class GeneticAlgorithm:
    def __init__(self, config: GeneticAlgorithmConfig, fitness_func: Callable):
        self.config = config
        self.fitness_func = fitness_func
        self.population: List[Individual] = []
        self.best_individual = None
        self.best_fitness = float('inf')
        self.solution_size = None
        
    def initialize_population(self, solution_size: int):
        """Initialize random population."""
        self.solution_size = solution_size
        self.population = []
        for _ in range(self.config.population_size):
            # Initialize with values suitable for timetabling
            # Every 3 values represent: day (0-4), period (0-7), room (0-7)
            chromosome = np.zeros(solution_size)
            for i in range(0, solution_size, 3):
                chromosome[i] = np.random.randint(0, 5)      # day
                chromosome[i+1] = np.random.randint(0, 8)    # period
                chromosome[i+2] = np.random.randint(0, 8)    # room
                
            individual = Individual(chromosome)
            individual.fitness = self.fitness_func(individual.chromosome)
            self.population.append(individual)
            
            # Update best if needed
            if individual.fitness < self.best_fitness:
                self.best_fitness = individual.fitness
                self.best_individual = Individual(individual.chromosome.copy())
                self.best_individual.fitness = individual.fitness
                
    def tournament_selection(self) -> Individual:
        """Select parent using tournament selection."""
        tournament = random.sample(self.population, self.config.tournament_size)
        return min(tournament, key=lambda x: x.fitness)
    
    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        """Perform crossover between two parents."""
        # Use uniform crossover
        mask = np.random.random(self.solution_size) < 0.5
        child_chromosome = np.where(mask, parent1.chromosome, parent2.chromosome)
        return Individual(child_chromosome)
    
    def mutate(self, individual: Individual):
        """Mutate an individual."""
        for i in range(0, len(individual.chromosome), 3):
            if np.random.random() < self.config.mutation_rate:
                individual.chromosome[i] = np.random.randint(0, 5)      # day
            if np.random.random() < self.config.mutation_rate:
                individual.chromosome[i+1] = np.random.randint(0, 8)    # period
            if np.random.random() < self.config.mutation_rate:
                individual.chromosome[i+2] = np.random.randint(0, 8)    # room
    
    def optimize(self, solution_size: int) -> np.ndarray:
        """Run genetic algorithm optimization."""
        # Initialize population
        self.initialize_population(solution_size)
        
        for generation in range(self.config.n_generations):
            new_population = []
            
            # Elitism: keep best individuals
            sorted_pop = sorted(self.population, key=lambda x: x.fitness)
            new_population.extend([Individual(x.chromosome.copy()) for x in sorted_pop[:self.config.elite_size]])
            
            # Generate rest of new population
            while len(new_population) < self.config.population_size:
                parent1 = self.tournament_selection()
                parent2 = self.tournament_selection()
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                child.fitness = self.fitness_func(child.chromosome)
                new_population.append(child)
                
                # Update best if needed
                if child.fitness < self.best_fitness:
                    self.best_fitness = child.fitness
                    self.best_individual = Individual(child.chromosome.copy())
                    self.best_individual.fitness = child.fitness
            
            self.population = new_population
        
        return self.best_individual.chromosome