# Simple differential evolution based on https://github.com/nathanrooy/differential-evolution-optimization
from random import random, sample, uniform, seed

import matplotlib.pyplot as plt


class DifferentialEvolution():

    def __init__(self, obj_func, bounds, popsize, differential_weight, crossover_prob, max_iterations):
        self.obj_func = obj_func
        self.bounds = bounds
        self.popsize = popsize
        self.agent_length = len(bounds)
        self.differential_weight = differential_weight
        self.crossover_prob = crossover_prob
        self.max_iter = max_iterations

        self.population = []
        self.improves = True

        # Statistics
        self.gen_obj_val = []
        self.iter_best_obj_val = []
        self.iter_best_agent = []
        self.iter_avg_obj_val = []
        self.num_gen = 0


        self.best_agent = None
        self.best_val = None

    def run(self, crossover="std",verbose=True):
        if crossover == 'points':
            crossover = self.crossover
        elif crossover == "std":
            crossover = self.crossover_on_points
        else:
            raise TypeError(f"Crossover {crossover} is not supported")
        
        self.init_population()

        # Interations
        for i in range(1, self.max_iter+1):
            self.improves = False
            if verbose:
                print("GENERATION:", i)

            self.gen_obj_val = []

            # A single generation
            for j, agent_target in enumerate(self.population):
                agent_donor = self.mutate(j)
                agent_trail = crossover(agent_donor, agent_target)
                self.selection(j, agent_target, agent_trail)

            # Statistics
            gen_avg_val = sum(self.gen_obj_val) / self.popsize
            gen_best_val = max(self.gen_obj_val)
            gen_best_agent = self.population[self.gen_obj_val.index(gen_best_val)]
        
            self.iter_avg_obj_val.append(gen_avg_val)
            self.iter_best_obj_val.append(gen_best_val)
            self.iter_best_agent.append(gen_best_agent.copy())

            # Stop if there is not improvement this generation
            if not self.improves:
                break
        self.num_gen = i
        self.best_obj_val = gen_best_val
        self.best_agent = gen_best_agent

    def init_population(self):
        # Initialize population
        self.population = []
        for i in range(self.popsize):
            agent = [uniform(lb, ub) for lb, ub in self.bounds]
            self.population.append(agent)

    def mutate(self, target_idx):
        # Select three parents excluding the target agent
        candidates_idx = list(range(self.popsize))
        candidates_idx.remove(target_idx)
        parents_idx = sample(candidates_idx, 3)

        parent1 = self.population[parents_idx[0]]
        parent2 = self.population[parents_idx[1]]
        parent3 = self.population[parents_idx[2]]

        # Calculate the solution best on parent1 + weighted difference between parent2 and parent3
        donor = [el1 + self.differential_weight *
                 (el2 - el3) for el1, el2, el3 in zip(parent1, parent2, parent3)]
        donor = self.ensure_bounds(donor)

        return donor

    def ensure_bounds(self, agent):
        # Saturate the solution such that it is within the bounds
        agent = [min(max(el, lb), ub)
                 for el, (lb, ub) in zip(agent, self.bounds)]
        return agent

    def crossover(self, agent1, agent2):
        # Standard crossover
        agent = []
        for i in range(self.agent_length):
            rng = random()
            if rng <= self.crossover_prob:
                agent.append(agent1[i])
            else:
                agent.append(agent2[i])
        return agent
    
    def crossover_on_points(self, agent1, agent2):
        # Crossover on points
        agents = []
        for i in range(0, self.agent_length, 2):
            rng = random()
            
            if rng <= self.crossover_prob:
                agent.append(agent1[i])
                agent.append(agent1[i+1])
            else:
                agent.append(agent2[i])
                agent.append(agent2[i+1])
        return agent
        

    def selection(self, agent_idx, agent, new_agent):
        # Greedy selection
        obj_val_agent = self.obj_func(agent)
        obj_val_new = self.obj_func(new_agent)

        # Maximization
        if obj_val_new > obj_val_agent:
            self.population[agent_idx] = new_agent
            self.gen_obj_val.append(obj_val_new)
            self.improves = True
        else:
            self.gen_obj_val.append(obj_val_agent)