# Simple differential evolution based on https://github.com/nathanrooy/differential-evolution-optimization
import matplotlib.pyplot as plt
import numpy as np

from random import random, randint, sample, uniform, seed
from copy import deepcopy
from time import time


from utils import Exitflag


class DifferentialEvolution():

    def __init__(self, obj_func, bounds, popsize, differential_weight, crossover_prob, init_bounds=None):
        self.obj_func = obj_func
        self.bounds = bounds
        self.init_bounds = init_bounds if init_bounds else bounds
        self.popsize = popsize
        self.agent_length = len(bounds)
        self.differential_weight = differential_weight
        self.crossover_prob = crossover_prob
        self.evaluations = 0

        self.population = []
        self.population_obj_values = []
        self.population_bottleneck_points = []
        self.improves = True # Flag the see if the population still improves within a generation
        
        self.optimum = None
        self.optimum_accuracy = None
        self.found_optimum = False
        self.exitflag = None

        # Statistics
        self.iter_best_obj_val = []
        self.iter_best_agent = []
        self.iter_avg_obj_val = []
        self.iter_var_obj_val = []
        self.iter_evals = []
        self.num_gen = 0

        self.iter_population = []

        self.best_agent = None
        self.best_val = None
        self.best_agent_idx = None
        
        # Initialize population
        self.init_population()
    
    def reset(self):
        self.evaluations = 0

        self.population = []
        self.population_obj_values = []
        self.population_bottleneck_points = []
        self.improves = True # Flag the see if the population still improves within a generation
        self.found_optimum = False
        self.exitflag = None

        # Statistics
        self.iter_best_obj_val = []
        self.iter_best_agent = []
        self.iter_avg_obj_val = []
        self.iter_var_obj_val = []
        self.iter_evals = []
        self.num_gen = 0

        self.iter_population = []

        self.best_agent = None
        self.best_val = None
        self.best_agent_idx = None
        
        self.init_population()

    def run(self, 
            crossover="std", 
            save_pop_each_iter=False, 
            stop_on_no_improvements=False, 
            stop_on_small_pop_diff=None,
            stop_on_no_improvements_gen_10=None,
            stop_on_small_pop_variance=None,
            max_evaluations=None, 
            max_generations=None,
            verbose=True):
        
        if crossover == 'best_points_rnd':
            crossover = self.crossover_best_points_rnd
        elif crossover == 'best_points4':
            crossover = self.crossover_best_points4
        elif crossover == 'best_points3':
            crossover = self.crossover_best_points3
        elif crossover == 'best_points2':
            crossover = self.crossover_best_points2
        elif crossover == 'points':
            crossover = self.crossover_on_points
        elif crossover == "std":
            crossover = self.crossover
        else:
            raise TypeError(f"Crossover {crossover} is not supported")
        
        start_time = time()

        # Initialize stop_on_no_improvements_gen_10 counters
        if stop_on_no_improvements_gen_10 is not None:
            obj_gen_0 = max(self.population_obj_values)
            gen_counter = 0    

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
                agent_cross = crossover(j, agent_target, agent_mutated)
                self.selection(j, agent_target, agent_cross)

            # Statistics
            gen_avg_val = sum(self.population_obj_values) / self.popsize
            gen_best_val = max(self.population_obj_values)
            gen_best_agent = self.population[self.population_obj_values.index(gen_best_val)]
        
            self.iter_var_obj_val.append(np.var(self.population_obj_values))
            self.iter_avg_obj_val.append(gen_avg_val)
            self.iter_best_obj_val.append(gen_best_val)
            self.iter_best_agent.append(gen_best_agent.copy())
            self.iter_evals.append(self.evaluations)
            self.best_agent_idx = self.population_obj_values.index(max(self.population_obj_values))

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
                print("\t{:<14}: {}".format("NUM POINTS", self.agent_length//2))
                print("\t{:<14}: {}".format("EVALUATIONS", self.evaluations))
                
                print("\t{:<14}: {}".format("AVG OBJ VAL", gen_avg_val))
                print("\t{:<14}: {}".format("BEST OBJ VAL", gen_best_val))
                
                if self.optimum is not None:
                    print("\t{:<14}: {}".format("OPTIMUM", self.optimum))
                
                print("\t{:<14}: {:.3f}s".format("GEN DURATION", end_time-gen_time))
                print("\t{:<14}: {:.3f}s".format("TOTAL TIME", end_time-start_time))


            # Stop if there is not improvement this generation
            if stop_on_no_improvements and not self.improves:
                self.exitflag = Exitflag.no_improvements
                print("No generational improvement")
                break            
            
            # Stop if the population has converges
            if (gen_best_val == gen_avg_val) \
                or (stop_on_small_pop_diff is not None \
                and abs(gen_best_val - gen_avg_val) < stop_on_small_pop_diff):
                self.exitflag = Exitflag.pop_converged
                print("Population converged")
                break

            # Stop if the improvements in 10 generations is smaller than stop_on_no_improvements_gen_10
            if stop_on_no_improvements_gen_10 is not None:
                gen_counter += 1
                if gen_counter >= 10:
                    if abs(gen_best_val - obj_gen_0) < stop_on_no_improvements_gen_10:
                        print("Improvements after 10 generation too small")
                        self.exitflag = Exitflag.no_improvements_gen_10
                        break
                    else:
                        obj_gen_0 = gen_best_val
                        gen_counter = 0
                        
            # Stops if the variance of the population is too small
            if stop_on_small_pop_variance is not None and np.var(self.population_obj_values) < stop_on_small_pop_variance:
                self.exitflag = Exitflag.pop_converged
                print("Population converged")
                break

            
            
            # Stop if the maximum number of evaluations has been reached
            if max_evaluations is not None and self.evaluations >= max_evaluations:
                self.exitflag = Exitflag.max_evals
                print("Maximum number of evaluations")
                break
            
            # Stop if the maximum number of generations has been reached
            if max_generations is not None and gen >= max_generations:
                self.exitflag = Exitflag.max_gen
                print("Maximum number of generations")
                break

            # Stop if the optimum has been reached
            if self.optimum is not None and self.is_optimum(gen_best_val):
                self.exitflag = Exitflag.optimum
                print("Optimum reached")
                break
            
            gen += 1

        self.num_gen = gen
        self.best_obj_val = gen_best_val
        self.best_agent = gen_best_agent
        

    def init_population(self):
        # Initialize population
        self.population = []
        for i in range(self.popsize):
            agent = [uniform(lb, ub) for lb, ub in self.init_bounds]
            agent_obj_val, bottleneck_points = self.obj_func(agent)
            self.evaluations += 1
            self.population.append(agent)
            self.population_obj_values.append(agent_obj_val)
            self.population_bottleneck_points.append(bottleneck_points)
            self.best_agent_idx = self.population_obj_values.index(max(self.population_obj_values))

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
    
    def crossover(self, target_idx, target, mutated):
        # Crossover 
        n = randint(0, self.agent_length-1)
        
        L = 1
        while random() < self.crossover_prob and L < self.agent_length - n:
            L += 1
        
        new_agent = target[:n] + mutated[n:n+L] + target[n+L:]
        return new_agent


    def crossover_on_points(self, target_idx, target, mutated):
        # Crossover on points 
        n = randint(0, (self.agent_length-2) / 2)*2
        
        L = 2
        while random() < self.crossover_prob and L < self.agent_length - n:
            L += 2
        
        new_agent = target[:n] + mutated[n:n+L] + target[n+L:]
        return new_agent


    def crossover_best_points2(self, target_idx, target, mutated):
        n = randint(0,1)

        bottleneck_points = self.population_bottleneck_points[target_idx]

        starting_point = bottleneck_points[n*2] # times 2 since for (x1,y1,x2,y2) it will selected either x1 or x2

        L = 2 # 2 to select both the x and y coordinates

        while random() < self.crossover_prob and L < self.agent_length - n:
            L += 2
        
        new_agent = target[:n] + mutated[n:n+L] + target[n+L:]
        return new_agent



    def crossover_best_points_rnd(self, target_idx, target, mutated):
        if random() < 0.5:
            # Use standard crossover 
            # return self.crossover(target_idx, target, mutated)
            return self.crossover_on_points(target_idx, target, mutated)

        n = randint(0, 2)

        # The points that "bottlenecks" the objective function
        x1, y1, x2, y2 = self.population_bottleneck_points[target_idx]

        new_agent = target.copy()
        if n == 0:
            # Replace both bottleneck points
            new_agent[x1] = mutated[x1]
            new_agent[y1] = mutated[y1]
            new_agent[x2] = mutated[x2]
            new_agent[y2] = mutated[y2]
        elif n == 1:
            # Only replace the first bottleneck point
            new_agent[x1] = mutated[x1]
            new_agent[y1] = mutated[y1]
        else:
            # Only replace the second bottleneck point
            new_agent[x2] = mutated[x2]
            new_agent[y2] = mutated[y2]
        return new_agent


    def crossover_best_points3(self, target_idx, target, mutated):
        # Crossover 
        n = randint(0, self.agent_length-1)
        
        L = 1
        while random() < self.crossover_prob and L < self.agent_length - n:
            L += 1
        
        new_agent = target[:n] + mutated[n:n+L] + target[n+L:]

        # The points that "bottlenecks" the objective function
        x1, y1, x2, y2 = self.population_bottleneck_points[target_idx]

        # If the "bottlenecks" have not changed then perform crossover on the bottleneck points
        if new_agent[x1] == target[x1] and new_agent[y1] == target[y1] \
            and new_agent[x2] == target[x2] and new_agent[y2] == target[y2]:
            n = randint(0, 2)
            if n == 0:
                # Replace both bottleneck points
                new_agent[x1] = mutated[x1]
                new_agent[y1] = mutated[y1]
                new_agent[x2] = mutated[x2]
                new_agent[y2] = mutated[y2]
            elif n == 1:
                # Only replace the first bottleneck point
                new_agent[x1] = mutated[x1]
                new_agent[y1] = mutated[y1]
            else:
                # Only replace the second bottleneck point
                new_agent[x2] = mutated[x2]
                new_agent[y2] = mutated[y2]
        return new_agent


    def crossover_best_points4(self, target_idx, target, mutated):
        # Crossover 
        if target_idx != self.best_agent_idx:
            return self.crossover(target_idx, target, mutated)

        n = randint(0, 2)

        # The points that "bottlenecks" the objective function
        x1, y1, x2, y2 = self.population_bottleneck_points[target_idx]

        new_agent = target.copy()
        if n == 0:
            # Replace both bottleneck points
            new_agent[x1] = mutated[x1]
            new_agent[y1] = mutated[y1]
            new_agent[x2] = mutated[x2]
            new_agent[y2] = mutated[y2]
        elif n == 1:
            # Only replace the first bottleneck point
            new_agent[x1] = mutated[x1]
            new_agent[y1] = mutated[y1]
        else:
            # Only replace the second bottleneck point
            new_agent[x2] = mutated[x2]
            new_agent[y2] = mutated[y2]
        return new_agent

        

    def selection(self, agent_idx, agent, new_agent):
        # Greedy selection
        obj_val_agent = self.population_obj_values[agent_idx]
        obj_val_new, bottleneck_points = self.obj_func(new_agent)
        self.evaluations += 1

        # Maximization
        if obj_val_new > obj_val_agent:
            self.population[agent_idx] = new_agent
            self.population_obj_values[agent_idx] = obj_val_new
            self.population_bottleneck_points[agent_idx] = bottleneck_points
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
        