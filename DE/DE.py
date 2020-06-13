# Simple differential evolution based on https://github.com/nathanrooy/differential-evolution-optimization
from random import random, randint, sample, uniform, seed
from copy import deepcopy
from time import time
import matplotlib.pyplot as plt


class DifferentialEvolution():

    def __init__(self, obj_func, bounds, popsize, differential_weight, crossover_prob):
        self.obj_func = obj_func
        self.bounds = bounds
        self.popsize = popsize
        self.agent_length = len(bounds)
        self.differential_weight = differential_weight
        self.crossover_prob = crossover_prob
        self.evaluations = 0

        self.population = []
        self.population_obj_values = []
        self.improves = True # Flag the see if the population still improves within a generation
        
        self.optimum = None
        self.optimum_accuracy = None
        self.found_optimum = False

        # Statistics
        self.iter_best_obj_val = []
        self.iter_best_agent = []
        self.iter_avg_obj_val = []
        self.num_gen = 0

        self.iter_population = []

        self.best_agent = None
        self.best_val = None
        
        # Initialize population
        self.init_population()
    
    def reset(self):
        self.evaluations = 0

        self.population = []
        self.population_obj_values = []
        self.improves = True # Flag the see if the population still improves within a generation
        self.found_optimum = False

        # Statistics
        self.iter_best_obj_val = []
        self.iter_best_agent = []
        self.iter_avg_obj_val = []
        self.num_gen = 0

        self.iter_population = []

        self.best_agent = None
        self.best_val = None
        
        self.init_population()

    def run(self, 
            crossover="std", 
            save_pop_each_iter=False, 
            stop_on_no_improvements=False, 
            stop_on_small_pop_diff=None,
            max_evaluations=None, 
            max_generations=None,
            verbose=True):
        
        if crossover == 'points':
            crossover = self.crossover_on_points
        elif crossover == "std":
            crossover = self.crossover
        else:
            raise TypeError(f"Crossover {crossover} is not supported")
        
        start_time = time()
        

        # Generations
        gen = 1
        while True:
            self.improves = False
            if verbose:
                gen_time = time()
                print("GENERATION:", gen)

            # A single generation
            for j, agent_target in enumerate(self.population):
                agent_mutated = self.mutate(j)
                agent_cross = crossover(agent_target, agent_mutated)
                self.selection(j, agent_target, agent_cross)

            # Statistics
            gen_avg_val = sum(self.population_obj_values) / self.popsize
            gen_best_val = max(self.population_obj_values)
            gen_best_agent = self.population[self.population_obj_values.index(gen_best_val)]
        
            self.iter_avg_obj_val.append(gen_avg_val)
            self.iter_best_obj_val.append(gen_best_val)
            self.iter_best_agent.append(gen_best_agent.copy())

            # Save the best 100 agents each population
            if save_pop_each_iter:
                obj_val_best_100 = sorted(self.population_obj_values, reverse=True)[:100]
                population_best_100 = [self.population[self.population_obj_values.index(obj_val)] for obj_val in obj_val_best_100]
                self.iter_population.append(deepcopy(population_best_100))

            # Print number of evaluations
            if verbose:
                end_time = time()
                # print("\tEVALUATIONS:", self.evaluations)
                # print("\tTIME \t\t:{}s".format(end_time-start_time))
                print("\t{:<14}: {}".format("DIMENSION", self.agent_length//2))
                print("\t{:<14}: {}".format("EVALUATIONS", self.evaluations))
                
                print("\t{:<14}: {}".format("AVG OBJ VAL", gen_avg_val))
                print("\t{:<14}: {}".format("BEST OBJ VAL", gen_best_val))
                
                if self.optimum is not None:
                    print("\t{:<14}: {}".format("OPTIMUM", self.optimum))
                
                print("\t{:<14}: {:.3f}s".format("GEN DURATION", end_time-gen_time))
                print("\t{:<14}: {:.3f}s".format("TOTAL TIME", end_time-start_time))


            # Stop if there is not improvement this generation
            if stop_on_no_improvements and not self.improves:
                print("No generational improvement")
                break

            # Stop if the max number of evaluations has been exceeded 
            if max_evaluations is not None and self.evaluations >= max_evaluations:
                print("Max number of evaluations")
                break
            
            # Stop if the optinum has been reached
            if self.optimum is not None and self.is_optimum(gen_best_val):
                print("Optimum reached")
                break
            
            # Stop if the population has converges
            if (gen_best_val == gen_avg_val) \
                or (stop_on_small_pop_diff is not None \
                and abs(gen_best_val - gen_avg_val) <= stop_on_small_pop_diff):
                print("Population converged")
                break
            
            
            # Stop if the maximum number of evaluations has been reached
            if max_evaluations is not None and self.evaluations >= max_evaluations:
                print("Maximum number of evaluations")
                break
            
            # Stop if the maximum number of generations has been reached
            if max_generations is not None and gen >= max_generations:
                print("Maximum number of generations")
                break
            
            gen += 1

        self.num_gen = gen
        self.best_obj_val = gen_best_val
        self.best_agent = gen_best_agent
        

    def init_population(self):
        # Initialize population
        self.population = []
        for i in range(self.popsize):
            agent = [uniform(lb, ub) for lb, ub in self.bounds]
            agent_obj_val = self.obj_func(agent)
            self.evaluations += 1
            self.population.append(agent)
            self.population_obj_values.append(agent_obj_val)

    def mutate(self, target_idx):
        # Select three parents excluding the target agent
        candidates_idx = list(range(self.popsize))
        candidates_idx.remove(target_idx)
        parents_idx = sample(candidates_idx, 3)

        parent1 = self.population[parents_idx[0]]
        parent2 = self.population[parents_idx[1]]
        parent3 = self.population[parents_idx[2]]

        # Calculate the solution best on parent1 + weighted difference between parent2 and parent3
        mutated = [el1 + self.differential_weight *
                 (el2 - el3) for el1, el2, el3 in zip(parent1, parent2, parent3)]
        mutated = self.ensure_bounds(mutated)

        return mutated

    def ensure_bounds(self, agent):
        # Saturate the solution such that it is within the bounds
        agent = [min(max(el, lb), ub)
                 for el, (lb, ub) in zip(agent, self.bounds)]
        return agent
    
    def crossover(self, target, mutated):
        # Crossover 
        n = randint(0, self.agent_length-1)
        
        L = 1
        while random() < self.crossover_prob and L < self.agent_length - n:
            L += 1
        
        new_agent = target[:n] + mutated[n:n+L] + target[n+L:]
        return new_agent
        

#     def crossover(self, agent1, agent2):
#         # Standard crossover
#         agent = []
#         for i in range(self.agent_length):
#             rng = random()
#             if rng <= self.crossover_prob:
#                 agent.append(agent1[i])
#             else:
#                 agent.append(agent2[i])
#         return agent
    
#     def crossover_on_points(self, agent1, agent2):
#         # Crossover on points
#         agents = []
#         for i in range(0, self.agent_length, 2):
#             rng = random()
            
#             if rng <= self.crossover_prob:
#                 agents.append(agent1[i])
#                 agents.append(agent1[i+1])
#             else:
#                 agents.append(agent2[i])
#                 agents.append(agent2[i+1])
#         return agents
        

    def selection(self, agent_idx, agent, new_agent):
        # Greedy selection
        obj_val_agent = self.population_obj_values[agent_idx]
        obj_val_new = self.obj_func(new_agent)
        self.evaluations += 1

        # Maximization
        if obj_val_new > obj_val_agent:
            self.population[agent_idx] = new_agent
            self.population_obj_values[agent_idx] = obj_val_new
            self.improves = True
            
            
    def set_optimum(self, optimum, accuracy):
        self.optimum = optimum
        self.optimum_accuracy = accuracy
        
        
    def is_optimum(self, obj_val):
        if abs(self.optimum - obj_val) <= self.optimum_accuracy:
            self.found_optimum = True
            return True
        else:
            return False
        