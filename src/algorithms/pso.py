"""
Particle Swarm Optimization (PSO) implementation.
"""
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Callable

@dataclass
class Particle:
    position: np.ndarray
    velocity: np.ndarray
    best_position: np.ndarray
    best_fitness: float

class PSO:
    def __init__(self,
                 n_particles: int = 100,
                 n_iterations: int = 200,
                 w_start: float = 0.9,  # Initial inertia weight
                 w_end: float = 0.4,    # Final inertia weight
                 c1: float = 2.0,       # Cognitive weight
                 c2: float = 2.0,       # Social weight
                 v_max: float = 4.0):   # Maximum velocity
        self.n_particles = n_particles
        self.n_iterations = n_iterations
        self.w_start = w_start
        self.w_end = w_end
        self.c1 = c1
        self.c2 = c2
        self.v_max = v_max
        self.w = w_start
        self.particles = []
        self.global_best_position = None
        self.global_best_fitness = float('inf')
        self.fitness_func = None
        self.solution_size = None
        
    def initialize_particles(self):
        """Initialize particles with random positions and velocities."""
        self.particles = []
        for _ in range(self.n_particles):
            # Initialize particle position (solution)
            position = np.random.uniform(0, 5, size=self.solution_size)  # Values will be rounded later
            velocity = np.random.uniform(-self.v_max, self.v_max, size=self.solution_size)
            
            particle = Particle(
                position=position.copy(),
                velocity=velocity,
                best_position=position.copy(),
                best_fitness=float('inf')
            )
            
            # Calculate initial fitness
            fitness = self.fitness_func(position)
            particle.best_fitness = fitness
            
            # Update global best if needed
            if fitness < self.global_best_fitness:
                self.global_best_fitness = fitness
                self.global_best_position = position.copy()
                
            self.particles.append(particle)
            
    def optimize(self, fitness_func: Callable, solution_size: int) -> np.ndarray:
        """Run PSO optimization."""
        self.fitness_func = fitness_func
        self.solution_size = solution_size
        self.initialize_particles()
        
        for iteration in range(self.n_iterations):
            # Update inertia weight
            self.w = self.w_start - (self.w_start - self.w_end) * iteration / self.n_iterations
            
            for particle in self.particles:
                # Update velocity
                r1, r2 = np.random.random(2)
                cognitive = self.c1 * r1 * (particle.best_position - particle.position)
                social = self.c2 * r2 * (self.global_best_position - particle.position)
                particle.velocity = (self.w * particle.velocity + cognitive + social)
                
                # Clamp velocity
                particle.velocity = np.clip(particle.velocity, -self.v_max, self.v_max)
                
                # Update position
                particle.position += particle.velocity
                
                # Calculate fitness
                fitness = self.fitness_func(particle.position)
                
                # Update personal best
                if fitness < particle.best_fitness:
                    particle.best_fitness = fitness
                    particle.best_position = particle.position.copy()
                    
                    # Update global best
                    if fitness < self.global_best_fitness:
                        self.global_best_fitness = fitness
                        self.global_best_position = particle.position.copy()
        
        return self.global_best_position